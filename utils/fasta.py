from Bio import SeqIO


def read_fasta(fasta_file) -> dict:
    """
    Read a fasta file and return a dictionary with the sequences.
    """
    sequences = {}
    for record in SeqIO.parse(fasta_file, "fasta"):
        sequences[record.id] = str(record.seq)
    return sequences


def check_fasta_format(fasta_text) -> bool:
    """检查 FASTA 格式是否正确"""
    if not fasta_text.startswith(">"):
        return False
    return True


def contain_short_sequence(sequence: dict) -> bool:
    """检查序列长度是否足够"""
    for seq_id, seq in sequence.items():
        if len(seq) < 35:
            return True
    return False


def contain_invalid_aa(sequence: dict) -> tuple:
    """检查是否包含非法氨基酸"""
    for seq_id, seq in sequence.items():
        if not set(seq).issubset(set("ACDEFGHIKLMNPQRSTVWY")):
            return True, seq_id
    return False, "Not contain"
