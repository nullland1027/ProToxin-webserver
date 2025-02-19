import io

import streamlit as st
import pandas as pd
import numpy as np


def is_valid_fasta(uploaded_file):
    """检查上传的文件是否是合法的 FASTA 格式"""
    if uploaded_file is None:
        return False, "No file uploaded."

    try:
        # 读取文件内容
        content = uploaded_file.getvalue().decode("utf-8").strip()
        lines = content.split("\n")

        # 1. 必须至少有一行，并且第一行必须以 '>' 开头
        if len(lines) == 0 or not lines[0].startswith(">"):
            return False, "Invalid FASTA format: First line must start with '>'."

        # 2. 检查序列部分是否只包含合法字符
        valid_chars = set("ACGTURYKMSWBDHVN-")  # 包括DNA/RNA常见字符和gap符号
        for line in lines[1:]:  # 跳过第一行
            if not set(line.upper()).issubset(valid_chars):
                return False, f"Invalid character found in sequence: {line}"
        return True, "Valid FASTA file."
    except Exception as e:
        return False, f"Error reading file: {str(e)}"



if __name__ == '__main__':
    st.title('ProToxin Prediction')
    fasta_file: io.BytesIO = st.file_uploader(
        label='Upload a file',
        type=['fasta'],
        accept_multiple_files=False,
    )



