import io
import os
import time
import pandas as pd

from config.config import Config as cfg
from config.config import Warn, Success, Error
from utils import fasta
from compute.features import FGenerator
from compute.predictor import do_predict
import streamlit as st

# 导入页面内容
from tabs.disclaimer import show_disclaimer
from tabs.about import show_about


# 自定义CSS来控制页面宽度
def set_page_container_style():
    # 自定义CSS来设置页面宽度为70%，并居中显示
    st.markdown(
        """
        <style>
        .block-container {
            max-width: 70% !important;
            padding-top: 2rem;
            padding-right: 1rem;
            padding-left: 1rem;
            padding-bottom: 3rem;
            margin: 0 auto;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def save_uploaded_file(uploaded_file):
    """保存上传的文件到本地，并返回文件路径"""
    if uploaded_file is None:
        return None
    file_path = os.path.join(cfg.FASTA_SAVE_DIR, uploaded_file.name)
    # 保存文件
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())  # 写入字节数据
    return file_path


def save_txt_to_file(file_name, content):
    """将内容写入本地文件"""
    file_path = os.path.join(cfg.FASTA_SAVE_DIR, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content + "\n")
    return file_path


def is_valid_sequence(fasta_file_path):
    if fasta_file_path:  # FASTA file has been saved in the server no matter file upload or text input
        try:
            sequences_dict = fasta.read_fasta(fasta_file_path)
            # 1. Empty or invalid string
            if len(sequences_dict["pid"]) == 0:
                st.error(Error.INVALID_FILE)
                st.stop()

            st.text(f"Number of sequences: {len(sequences_dict['pid'])}")
            # 2. Check sequence length
            if fasta.contain_short_sequence(sequences_dict):
                st.warning(Warn.TOO_SHORT_SEQUENCE)
                sequences_dict = None  # Reset sequences_dict
                st.stop()

            # 3. Check ambiguous amino acids
            invalid_aa, seq_id = fasta.contain_invalid_aa(sequences_dict)
            if invalid_aa:
                st.error(f"{Error.INVALID_AA} Found in sequence: {seq_id}")
                sequences_dict = None  # Reset sequences_dict
                st.stop()
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            st.stop()
        return sequences_dict
    return None


def show_sequence(sequences_dict):
    st.dataframe(pd.DataFrame({
        "Protein ID": list(sequences_dict["pid"]),
        "Sequence": list(sequences_dict["seq"])
    }))


def gen_features(fasta_file_path):
    fg = FGenerator(
        fasta_file=fasta_file_path,
        feature_selection_file="config/fs_88_2024-10-23-10:06:41.json",
        protr_features_file="config/selected_protr_features.json",
        protein_db_path="data/uniprot_sprot_db_20240911/uniprot_sprot_db"
    )
    fg.gen_protr()
    fg.gen_pssm()
    fg.gen_aaindex()
    fg.combine_features()
    fg.feature_select()
    return fg.get_data_in_dataframe()


def predict_toxin(fasta_file_path):
    with st.status("Running...", expanded=True) as status:
        st.write("Fetching data...")
        time.sleep(0.5)
        st.write("Feature generating...")
        feature_df = gen_features(fasta_file_path)
        st.write("Model predicting...")
        time.sleep(1)
        status.update(
            label="Prediction complete!", state="complete", expanded=False
        )
        st.toast('Finished!', icon='🎉')
        return feature_df


def show_result(df):
    # 创建 3 列，并将 DataFrame 放在中间列
    col1, col2, col3 = st.columns([1, 18, 1])
    with col2:
        st.dataframe(df, use_container_width=True)


def welcome_section():
    """显示欢迎信息的函数"""
    st.title('Welcome to ProToxin')

    st.markdown("""
    ProToxin is a machine learning-based predictor for detecting protein toxins from sequences. 
    It is based on a machine learning algorithm, gradient boosting. ProToxin is a fast and efficient 
    method and is freely available. It can be used for small and large numbers of sequences.

    ProToxin was developed in the groups of Prof. Yang Yang (add here the address) and 
    Prof. Mauno Vihinen, Protein Structure and Bioinformatics Research group, Lund University, Sweden.
    """)

    st.divider()


def prediction_page():
    """预测功能页面"""
    # 添加页面标题
    st.subheader('Protein Toxin Prediction')

    # 使用 session_state 初始化持久化变量
    if "fasta_file_path" not in st.session_state:
        st.session_state.fasta_file_path = None
    if "sequences_dict" not in st.session_state:
        st.session_state.sequences_dict = None

    # 选项：上传文件 or 输入文本
    option = st.radio("Choose an input method:", ("Upload a file", "Enter sequence manually"))
    if option == "Upload a file":
        upload_file: io.BytesIO = st.file_uploader(
            label='Upload a file',
            type=['fasta'],
            accept_multiple_files=False,
        )
        if upload_file:
            st.session_state.fasta_file_path = save_uploaded_file(upload_file)
            st.success(Success.FILE_UPLOAD)
    elif option == "Enter sequence manually":
        fasta_text = st.text_area("Enter your FASTA content here:")
        if st.button("Submit"):
            if fasta.check_fasta_format(fasta_text.strip()):
                file_name = "manual_input.fasta"
                st.session_state.fasta_file_path = save_txt_to_file(file_name, fasta_text)
                st.success(f"{Success.TEXT_UPLOAD}")
            else:
                st.warning(Warn.NOT_FASTA_FORMAT)

    # 使用 session_state 中保存的 fasta_file_path 进行验证
    st.session_state.sequences_dict = is_valid_sequence(st.session_state.fasta_file_path)

    st.divider() # ---------------------------------------------------

    if st.session_state.sequences_dict:
        st.subheader("Sequence Information: ")
        show_sequence(st.session_state.sequences_dict)
        st.divider()
        if st.button("Start"):
            st.text(st.session_state.fasta_file_path)
            try:
                df = predict_toxin(st.session_state.fasta_file_path)
                st.divider()
                st.header("Prediction Result")
                res = do_predict(df)
                show_result(res)
            except Exception as e:
                st.error(f"Error: {str(e)}")


def home_page():
    """主页内容"""
    welcome_section()
    prediction_page()


if __name__ == '__main__':
    # 设置页面配置
    st.set_page_config(
        page_title="ProToxin",
        layout="centered",  # 改回居中布局，我们将通过自定义CSS控制具体宽度
    )

    # 应用自定义宽度设置
    set_page_container_style()

    os.makedirs(cfg.FASTA_SAVE_DIR, exist_ok=True)

    # 使用Streamlit原生的选项卡组件创建导航
    tab1, tab2, tab3 = st.tabs(["Home", "Disclaimer", "About"])

    with tab1:
        home_page()

    with tab2:
        show_disclaimer()

    with tab3:
        show_about()
