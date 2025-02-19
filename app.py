import io
import os
import random
import time
import pandas as pd

from config import Config as cfg
from config import Warn, Success, Error
from utils import fasta
import streamlit as st


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
        f.write(content)
    return file_path


def is_valid_sequence(fasta_file_path):
    if fasta_file_path:  # FASTA file has been saved in the server no matter file upload or text input
        try:
            sequences_dict = fasta.read_fasta(fasta_file_path)
            # 1. Empty or invalid string
            if len(sequences_dict) == 0:
                st.error(Error.INVALID_FILE)
                st.stop()

            st.text(f"Number of sequences: {len(sequences_dict)}")
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
        "Protein ID": list(sequences_dict.keys()),
        "Sequence": list(sequences_dict.values())
    }))


def predict_toxin(sequence):
    with st.status("Running...", expanded=True) as status:
        st.write("Searching for data...")
        time.sleep(2)  # TODO
        st.write("Feature generating...")
        time.sleep(1)  # TODO
        st.write("Downloading data...")
        time.sleep(1)
        status.update(
            label="Prediction complete!", state="complete", expanded=False
        )
        st.toast('Finished!', icon='🎉')


def show_result(result):
    df = pd.DataFrame(
        {
            "Protein ID": list(range(0, 10)),
            "Toxin Probability": list(range(0, 10)),
            "Toxin Type": ["Type 1"] * 5 + ["Type 2"] * 5,
        }
    )
    st.dataframe(df)


if __name__ == '__main__':
    st.title('ProToxin Prediction')
    os.makedirs(cfg.FASTA_SAVE_DIR, exist_ok=True)

    # Initialize variables
    fasta_file_path = None
    sequences_dict = None

    # 选项：上传文件 or 输入文本
    option = st.radio("Choose an input method:", ("Upload a file", "Enter sequence manually"))
    if option == "Upload a file":
        upload_file: io.BytesIO = st.file_uploader(
            label='Upload a file',
            type=['fasta'],
            accept_multiple_files=False,
        )
        if upload_file:
            fasta_file_path = save_uploaded_file(upload_file)
            st.success(Success.FILE_UPLOAD)
    elif option == "Enter sequence manually":
        fasta_text = st.text_area("Enter your FASTA content here:")
        if st.button("Submit"):
            if fasta.check_fasta_format(fasta_text.strip()):
                file_name = "manual_input.fasta"
                fasta_file_path = save_txt_to_file(file_name, fasta_text)
                st.success(Success.TEXT_UPLOAD)
            else:
                st.warning(Warn.NOT_FASTA_FORMAT)
        else:
            fasta_file_path = None

    sequences_dict = is_valid_sequence(fasta_file_path)

    st.divider() # ---------------------------------------------------

    if sequences_dict:
        show_sequence(sequences_dict)
        st.divider()
        if st.button("Start"):
            predict_toxin(sequences_dict)
            st.divider()
            st.header("Prediction Result")
            show_result(None)
