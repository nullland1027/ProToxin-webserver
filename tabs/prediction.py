import io
import os
import time
import pandas as pd
import streamlit as st

from config.config import Config as cfg
from config.config import Warn, Success, Error
from utils import fasta
from compute.features import FGenerator
from compute.predictor import do_predict

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

            # 检查序列数量是否超过100
            if len(sequences_dict['pid']) > 100:
                st.error(Error.TOO_MANY_SEQUENCES)
                st.stop()

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
    st.dataframe(
        pd.DataFrame({
            "Protein ID": list(sequences_dict["pid"]),
            "Sequence": list(sequences_dict["seq"])
        }),
        use_container_width=True,  # 使表格使用容器的全宽
        hide_index=True,  # 隐藏索引以使表格更整洁
    )


# 移除 @st.cache_data 装饰器以解决错误
def gen_features(fasta_file_path, _progress_callback=None):
    fg = FGenerator(
        fasta_file=fasta_file_path,
        feature_selection_file="config/fs_88_2024-10-23-10:06:41.json",
        protr_features_file="config/selected_protr_features.json",
        protein_db_path="data/uniprot_sprot_db_20240911/uniprot_sprot_db"
    )
    # 按顺序生成三种特征，每种都调用相同的进度回调
    fg.gen_protr(progress_callback=_progress_callback)
    fg.gen_pssm(progress_callback=_progress_callback)
    fg.gen_aaindex(progress_callback=_progress_callback)
    fg.combine_features()
    fg.feature_select()
    return fg.get_data_in_dataframe()


def predict_toxin(fasta_file_path):
    with st.status("Running...", expanded=True) as status:
        st.write("Fetching data...")
        time.sleep(0.5)
        st.write("Feature generating...")

        # 获取序列数量以计算总迭代次数
        from utils.fasta import how_many_seqs
        seq_count = how_many_seqs(fasta_file_path)

        # 三种特征（protr、PSSM、aaindex）的总迭代次数是序列数的3倍
        total_iterations = seq_count * 3
        current_iteration = 0

        # 创建单一进度条
        progress_bar = st.progress(0)
        progress_text = st.empty()

        # 每次有一个序列特征计算完成时，更新进度条
        def update_progress():
            nonlocal current_iteration
            current_iteration += 1
            progress = current_iteration / total_iterations
            # 更新进度条和文本
            progress_bar.progress(progress)
            progress_text.text(f"{int(progress*100)}%")

        feature_df = gen_features(
            fasta_file_path,
            _progress_callback=update_progress
        )

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


def show_prediction():
    """预测功能页面"""
    # 添加页面标题
    st.title('Protein Toxin Prediction')

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
