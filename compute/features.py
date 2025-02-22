import os
import contextvars
from concurrent.futures import ThreadPoolExecutor

import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri, conversion, default_converter

import pandas as pd
from features.pssm import create_pssm
from features.aaidx import get_important_aaindex_617_by_fasta
from utils.fasta import how_many_seqs
import json

pandas2ri.activate()


class FGenerator:
    def __init__(self, fasta_file: str, feature_selection_file: str, protr_features_file: str, protein_db_path: str):
        self.fasta_file = fasta_file
        self.fs_json = feature_selection_file
        self.__db_path = protein_db_path
        self.seq_num = how_many_seqs(fasta_file)

        with open(protr_features_file, "r") as file:
            self.protr_features = json.load(file)

        self.__r_script_path = {
            "aac":    "features/protr/protr_aac.R",
            "apaac":  "features/protr/protr_apaac.R",
            "ctd":    "features/protr/protr_ctd.R",
            "ctriad": "features/protr/protr_ctriad.R",
            "dpc":    "features/protr/protr_dpc.R",
            "geary":  "features/protr/protr_geary.R",
            "mb":     "features/protr/protr_mb.R",
            "qso":    "features/protr/protr_qso.R"
        }
        self.df_aac = None
        self.df_apaac = None
        self.df_ctd = None
        self.df_ctriad = None
        self.df_dpc = None
        self.df_geary = None
        self.df_mb = None
        self.df_qso = None
        self.df_protr = None

        self.df_pssm = None
        self.df_aaindex = None

        self.df_total = None

    def _gen_aac(self):
        r_script_path = self.__r_script_path["aac"]
        cols = self.protr_features["aac"]
        with open(r_script_path, "r") as file:
            r_code = file.read()

        try:
            with conversion.localconverter(default_converter):
                robjects.r.assign("fasta_file", self.fasta_file)  # 将 Python 参数传递到 R 脚本
                result = robjects.r(r_code)  # 返回值是 R 的数据框
                processed_data = pandas2ri.rpy2py(result)  # 将 R 数据框转换为 Pandas 数据框
                self.df_aac = pd.DataFrame(processed_data, columns=cols)
        except Exception as e:
            print(f"Error while executing R script: {e}")

    def _gen_apaac(self):
        """
        Does not support too short sequences.
        'Pc1.N', 'Pc1.A', 'Pc1.C'
        Length of the protein sequence must be greater than "lambda"
        """
        r_script_path = self.__r_script_path["apaac"]
        cols = self.protr_features["apaac"]
        with open(r_script_path, "r") as file:
            r_code = file.read()

        try:
            with conversion.localconverter(default_converter):
                robjects.r.assign("fasta_file", self.fasta_file)
                result = robjects.r(r_code)
                processed_data = pandas2ri.rpy2py(result)
                self.df_apaac = pd.DataFrame(processed_data, columns=cols)
        except Exception as e:
            print(f"Error while executing R script: {e}")

    def _gen_ctd(self):
        r_script_path = self.__r_script_path["ctd"]
        cols = self.protr_features["ctd"]
        with open(r_script_path, "r") as file:
            r_code = file.read()

        try:
            with conversion.localconverter(default_converter):
                robjects.r.assign("fasta_file", self.fasta_file)
                result = robjects.r(r_code)
                processed_data = pandas2ri.rpy2py(result)
                self.df_ctd = pd.DataFrame(processed_data, columns=cols)
        except Exception as e:
            print(f"Error while executing R script: {e}")

    def _gen_ctriad(self):
        r_script_path = self.__r_script_path["ctriad"]
        cols = self.protr_features["ctriad"]
        with open(r_script_path, "r") as file:
            r_code = file.read()

        try:
            with conversion.localconverter(default_converter):
                robjects.r.assign("fasta_file", self.fasta_file)
                result = robjects.r(r_code)
                processed_data = pandas2ri.rpy2py(result)
                self.df_ctriad = pd.DataFrame(processed_data, columns=cols)
        except Exception as e:
            print(f"Error while executing R script: {e}")

    def _gen_dpc(self):
        r_script_path = self.__r_script_path["dpc"]
        cols = self.protr_features["dpc"]
        with open(r_script_path, "r") as file:
            r_code = file.read()

        try:
            with conversion.localconverter(default_converter):
                robjects.r.assign("fasta_file", self.fasta_file)
                result = robjects.r(r_code)
                processed_data = pandas2ri.rpy2py(result)
                self.df_dpc = pd.DataFrame(processed_data, columns=cols)
        except Exception as e:
            print(f"Error while executing R script: {e}")

    def _gen_geary(self):
        r_script_path = self.__r_script_path["geary"]
        cols = self.protr_features["geary"]
        with open(r_script_path, "r") as file:
            r_code = file.read()

        try:
            with conversion.localconverter(default_converter):
                robjects.r.assign("fasta_file", self.fasta_file)
                result = robjects.r(r_code)
                processed_data = pandas2ri.rpy2py(result)
                self.df_geary = pd.DataFrame(processed_data, columns=cols)
        except Exception as e:
            print(f"Error while executing R script: {e}")

    def _gen_mb(self):
        r_script_path = self.__r_script_path["mb"]
        cols = self.protr_features["mb"]
        with open(r_script_path, "r") as file:
            r_code = file.read()

        try:
            with conversion.localconverter(default_converter):
                robjects.r.assign("fasta_file", self.fasta_file)
                result = robjects.r(r_code)
                processed_data = pandas2ri.rpy2py(result)
                self.df_mb = pd.DataFrame(processed_data, columns=cols)
        except Exception as e:
            print(f"Error while executing R script: {e}")

    def _gen_qso(self):
        """
        'Schneider.Xd.28', 'Schneider.Xd.27' missing
        Does not support too short sequences.
        Length of the protein sequence must be greater than `nlag`
        """
        r_script_path = self.__r_script_path["qso"]
        cols = self.protr_features["qso"]
        with open(r_script_path, "r") as file:
            r_code = file.read()

        try:
            with conversion.localconverter(default_converter):
                robjects.r.assign("fasta_file", self.fasta_file)
                result = robjects.r(r_code)
                processed_data = pandas2ri.rpy2py(result)
                self.df_qso = pd.DataFrame(processed_data, columns=cols)
        except Exception as e:
            print(f"Error while executing R script: {e}")

    def gen_protr(self):
        self._gen_aac()
        self._gen_apaac()
        self._gen_ctd()
        self._gen_ctriad()
        self._gen_dpc()
        self._gen_geary()
        self._gen_mb()
        self._gen_qso()
        self.df_aac.reset_index(drop=True, inplace=True)
        self.df_apaac.reset_index(drop=True, inplace=True)
        self.df_ctd.reset_index(drop=True, inplace=True)
        self.df_ctriad.reset_index(drop=True, inplace=True)
        self.df_dpc.reset_index(drop=True, inplace=True)
        self.df_geary.reset_index(drop=True, inplace=True)
        self.df_mb.reset_index(drop=True, inplace=True)
        self.df_qso.reset_index(drop=True, inplace=True)
        self.df_protr = pd.concat([self.df_aac, self.df_apaac, self.df_ctd, self.df_ctriad,
                                   self.df_dpc, self.df_geary, self.df_mb, self.df_qso], axis=1)


    def gen_pssm(self):
        self.df_pssm = create_pssm(self.fasta_file, self.__db_path, evalue=0.001, num_iterations=3, n_jobs=os.cpu_count())

    def gen_aaindex(self):
        self.df_aaindex = get_important_aaindex_617_by_fasta(self.fasta_file)

    def combine_features(self):
        self.df_total = pd.concat([self.df_pssm, self.df_protr, self.df_aaindex], axis=1)

    def feature_select(self):
        with open(self.fs_json, "r") as file:
            fs = json.load(file)
        self.df_total = self.df_total[fs["Selected features"]]
        self.df_total = pd.concat([self.df_pssm["pid"], self.df_total], axis=1)

    def get_data_in_dataframe(self) -> pd.DataFrame:
        return self.df_total