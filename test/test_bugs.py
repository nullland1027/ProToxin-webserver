import unittest
import utils.fasta as fasta

class TestBugs(unittest.TestCase):
    def test_seq_length_false(self):
        d = {
            "seq1": "ACDEFGHIKLMNPQRSTVWYACDEFGHIKLMNPQRSTVWYACDEFGHIKLMNPQRSTVWY",
            "seq2": "ACDEFGHIKLMN",
        }
        self.assertEqual(fasta.contain_short_sequence(d), False)

    def test_seq_length_true(self):
        d = {
            "seq1": "ACDEFGHIKLMNPQRSTVWYACDEFGHIKLMNPQRSTVWYACDEFGHIKLMNPQRSTVWY",
            "seq2": "ACDEFGHIKLMNPQRSTVWYACDEFGHIKLMNPQRSTVWYACDEFGHIKLMNPQRSTVWYACDEFGHIKLMNPQRSTVWY",
        }
        self.assertEqual(fasta.contain_short_sequence(d), True)