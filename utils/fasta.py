import pandas as pd
from Bio import SeqIO


def read_fasta(fasta_file) -> dict:
    """
    Read a fasta file and return a dictionary with the sequences.
    """
    sequences = {
        "pid": [],
        "seq": []
    }
    for record in SeqIO.parse(fasta_file, "fasta"):
        sequences["pid"].append(str(record.id))
        sequences["seq"].append(str(record.seq))
    return sequences


def check_fasta_format(fasta_text) -> bool:
    """检查 FASTA 格式是否正确"""
    if not fasta_text.startswith(">"):
        return False
    return True


def contain_short_sequence(sequence: dict) -> bool:
    """检查序列长度是否足够"""
    for seq in sequence["seq"]:
        if len(seq) < 35:
            return True
    return False


def contain_invalid_aa(sequence: dict) -> tuple:
    """检查是否包含非法氨基酸"""
    for i in range(len(sequence["seq"])):
        if not set(sequence["seq"][i]).issubset(set("ACDEFGHIKLMNPQRSTVWY")):
            return True, sequence["pid"][i]
    return False, "Not contain"


def how_many_seqs(seq_file: str) -> int:
    """
    Count how many sequences in the file
    :param seq_file: fasta or csv file
    :return: the length
    """
    if seq_file.endswith("fasta"):
        count = 0
        for record in SeqIO.parse(seq_file, "fasta"):
            count += 1
        return count
    elif seq_file.endswith("csv"):
        return len(pd.read_csv(seq_file))
