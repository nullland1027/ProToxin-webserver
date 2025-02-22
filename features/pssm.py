import os
import pandas as pd
from tqdm.auto import tqdm
from Bio import SeqIO
import numpy as np
import time
from functools import wraps

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

blast = "https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.16.0+-x64-linux.tar.gz"
header = list("A  R  N  D  C  Q  E  G  H  I  L  K  M  F  P  S  T  W  Y  V".replace(" ", ""))
header = [f"PSSM_{aa}" for aa in header]
MOST_IMPORTANT_OF_88 = ["PSSM_W", "PSSM_C", "PSSM_Q", "PSSM_S", "PSSM_N", "PSSM_G", "PSSM_F", "PSSM_A"]


def retry_on_failure(retries=5, delay=1):
    """
    装饰器，用于重试失败的函数。
    :param retries: 最大重试次数。
    :param delay: 每次重试之间的延迟时间（秒）。
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                result = func(*args, **kwargs)
                if result:  # 如果函数成功返回结果，则直接返回
                    return result
                time.sleep(delay)  # 等待后重试
            return False  # 如果重试多次仍失败，返回 False
        return wrapper
    return decorator


@retry_on_failure(retries=3, delay=1)
def check_file_exists(filepath):
    """
    检查文件是否存在。
    :param filepath: 文件路径。
    :return: 文件存在则返回 True，否则返回 False。
    """
    return os.path.exists(filepath)


def extract_pssm_from_file(pssm_file) -> list:
    """
    从PSSM文件中，提取前20列纯数字矩阵。如果未命中，无法提取到PSSM文件，返回空列表
    :param pssm_file:
    :return: 2d array
    """
    pssm = []
    if os.path.exists(pssm_file):
        with open(pssm_file, 'r') as file:
            lines = file.readlines()
            # 跳过前3行的头部
            for line in lines[3:]:
                # 遇到空行直接结束读取
                if not line.strip():
                    break
                # 处理中间的数据行
                try:
                    scores = line.split()[2:22]  # 提取前20列
                    pssm.append([int(score) for score in scores])  # 转换为整数并添加
                except ValueError:
                    # 如果某一行格式不对，则忽略该行
                    continue
    return pssm


def global_average_pooling(pssm: np.ndarray) -> np.ndarray:
    """
    全局平均池化，压缩PSSM到1D长度为20的向量
    :param pssm: (n, 20) ndarray
    """
    if pssm.size == 0:
        raise ValueError("Empty PSSM")
    return np.mean(pssm, axis=0)


def create_pssm(fasta_file, prot_db_path, evalue=0.001, num_iterations=3, n_jobs=1) -> pd.DataFrame:
    """
    1. Extract one sequence from the fasta file.
    2. Write the sequence to a temporary fasta file.
    3. Run psiblast on the temporary fasta file. To generate the PSSM file.
    4. Extract the PSSM from the PSSM file.
    5. Perform global average pooling on the PSSM.
    6. Save the PSSM to a csv file.
    """

    columns = ["pid"] + MOST_IMPORTANT_OF_88
    dtypes = {
        "pid": 'string'
    }
    for col in MOST_IMPORTANT_OF_88:
        dtypes[col] = 'float32'
    pssm_df = pd.DataFrame({col: pd.Series(dtype=dtype) for col, dtype in dtypes.items()})
    records = SeqIO.parse(fasta_file, "fasta")
    for record in tqdm(records, total=len(list(SeqIO.parse(fasta_file, "fasta"))), dynamic_ncols=True, colour="red"):
        file_name = f"{record.id}.fasta".replace("|", "-")  # 生成文件名，使用序列的ID
        tmp_fasta_file = os.path.join("tmp", file_name)  # fasta file path
        SeqIO.write(record, tmp_fasta_file, "fasta")  # 提取单个序列，并写入文件
        pssm_file = os.path.join("tmp", str(record.id).replace("|", "-") + ".pssm")
        os.system(
            f"""psiblast -query {tmp_fasta_file} \
            -db {prot_db_path} \
            -evalue {evalue} \
            -num_iterations {num_iterations} \
            -num_threads {n_jobs} \
            -out_ascii_pssm {pssm_file} \
            -sum_stats 0 \
            -comp_based_stats 0 \
            -out results.txt""")

        try:
            if not check_file_exists(pssm_file):
                raise FileNotFoundError
            data = np.array(extract_pssm_from_file(pssm_file))         # 如果没有文件，pssm_file会返回一个空列表
            pooled_data = global_average_pooling(data).reshape(1, -1)  # 如果没有文件，会返回一个[[nan]]
            df = pd.DataFrame(pooled_data, columns=header)[MOST_IMPORTANT_OF_88]
            os.remove(tmp_fasta_file)
            os.remove(pssm_file)
        except FileNotFoundError as _:  # 没有找到PSSM文件
            data = np.array([np.nan] * 20).reshape(1, -1)
            df = pd.DataFrame(data, columns=header)[MOST_IMPORTANT_OF_88]
        except ValueError as _:
            pass
        df = pd.concat([pd.DataFrame([record.id], columns=["pid"]), df], axis=1)
        pssm_df = pd.concat([pssm_df, df], axis=0, ignore_index=True)
    return pssm_df


def save_pssm2csv(fasta_file, output_path, filename, prot_db_path, evalue=0.001, num_iterations=3, n_jobs=1):
    pssm_df = create_pssm(fasta_file, prot_db_path, evalue, num_iterations, n_jobs)
    pssm_df.to_csv(str(os.path.join(output_path, filename)), index=False)

if __name__ == '__main__':
    fasta = "data/sequences/final_TRAIN/v4/neg_train_all_part11.fasta"
    output = "data/dataset/train/v4/pssm"
    db = "/home/whoami/uniprot_sprot_db_20240911/uniprot_sprot_db"  # mars
    save_pssm2csv(fasta, output, "test", db, n_jobs=16)
