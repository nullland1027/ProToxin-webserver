class Config:
    FASTA_SAVE_DIR = 'upload'


class Warn:
    NOT_FASTA_FORMAT = "⚠️ Please enter protein sequence in FASTA format."
    TOO_SHORT_SEQUENCE = "⚠️ The sequence is too short. Please enter sequences with at least 35 amino acids."

class Success:
    FILE_UPLOAD = "✅ File uploaded successfully."
    TEXT_UPLOAD = "✅ Text uploaded successfully."

class Error:
    INVALID_FILE = "❌ Invalid FASTA file."
    INVALID_AA = "❌ Invalid amino acids found in the sequence. Should remove BJOUXZ."