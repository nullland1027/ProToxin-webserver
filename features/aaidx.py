from collections import defaultdict
import numpy as np
import json
import pandas as pd
from utils import fasta


a_list = ('A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y')
aa_list = [i + j for i in a_list for j in a_list]


with open("config/selected_aaindex_features.json", "r") as file:
    MOST_IMPORTANT_AAINDEX_OF_88 = json.load(file)["aaindex"]


def check_aa(seq, aa):
    seq = "".join(seq.split())
    aaf = aa[0]          # from
    aai = int(aa[1:-1])  # index
    aat = aa[-1]         # to
    if aaf not in a_list:
        raise RuntimeError("aa error, origin of aa is invalid.")
    if aat not in a_list:
        raise RuntimeError("aa error, nutation of aa is invalid.")
    if aai < 1 or aai > len(seq):
        raise RuntimeError("aa error, index of aa is invalid.")
    if seq[aai - 1] != aaf:
        raise RuntimeError("aa error, seq[{}] = {}, but origin of aa = {}".format(aai, seq[aai - 1], aaf))

    return seq, aaf, aat, aai


def get_aaindex(seq, aa):
    seq, aaf, aat, aai = check_aa(seq, aa)
    aaindex = pd.read_csv(
        filepath_or_buffer='data/aaindex_db/aaindexmatrix_23.txt',
        sep="\t",
        header=None,
        names=['name'] + aa_list,
        index_col='name'
    ).T
    res = aaindex.loc["{}{}".format(aaf, aat), :]
    return res.to_dict()


def get_aaindex1_feature_matrix_by_seq(seq):
    """
    return shape (length, 566)
    :param seq:
    :return:
    """
    matrix = []
    df_aaindex1 = pd.read_csv("../../data/database/aaindex_db/aaindex1.csv")
    for aa in seq:
        matrix.append(df_aaindex1[aa].values)
    return np.mean(np.array(matrix), axis=0)


def get_aaindex_617(seq):
    aaindex1_in_617 = pd.read_csv("data/aaindex_db/aaindex1_in_617.csv")
    df1 = []
    for aa in seq:
        df1.append(aaindex1_in_617[aa])
    df1 = pd.DataFrame(df1)
    df1.columns = aaindex1_in_617["cate"].tolist()
    df1.reset_index(drop=True, inplace=True)
    res1 = df1.mean().to_frame().T

    df2 = defaultdict(int)
    for i in range(1, len(seq) + 1):
        res = get_aaindex(seq, f"{seq[i - 1]}{i}{seq[i - 1]}")
        for k, v in res.items():
            df2[k] += v
    df2 = {key: [value / len(seq)] for key, value in df2.items()}
    res2 = pd.DataFrame(df2)

    return pd.concat([res1, res2], axis=1)


def get_aaindex_617_by_fasta(fasta_file, progress_callback=None):
    d = fasta.read_fasta(fasta_file)
    res = []
    sequences = d["seq"]
    total_seqs = len(sequences)
    for i, seq in enumerate(sequences):
        res.append(get_aaindex_617(seq))
        if progress_callback:
            progress_callback(i + 1, total_seqs)
    df = pd.concat(res, axis=0, ignore_index=True)
    df.insert(0, "protein_id", d["pid"])
    return df


def get_important_aaindex_617_by_fasta(fasta_file, progress_callback=None):
    df = get_aaindex_617_by_fasta(fasta_file, progress_callback=progress_callback)
    return df[MOST_IMPORTANT_AAINDEX_OF_88]


if __name__ == '__main__':
    fasta_f = "data/sequences/final_TRAIN/v4/neg_train_all.fasta"
    get_important_aaindex_617_by_fasta(fasta_f).to_csv("data/dataset/train/v4/aaindex/neg_aaindex_all.csv", index=False)
    print("done")
