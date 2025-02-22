import joblib
import numpy as np



def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class LGBMPredictor:
    def __init__(self, model_file):
        self.lgb_model = joblib.load(model_file)
        self.result = None

    def predict(self, df):
        X = np.ascontiguousarray(df.iloc[:, 1:].values)  # Remove protein ID
        self.result = sigmoid(self.lgb_model.predict(X, raw_score=True))
        res_d = {
            "Index": list(range(1, len(self.result) + 1)),
            "Protein ID": df.iloc[:, 0].values,
            "Probability": self.result,
            "Prediction result": ["Toxin" if i >= 0.5 else "Non-toxin" for i in self.result]
        }
        return res_d


def do_predict(dataframe):
    p = LGBMPredictor("data/model/LGBM_2025-02-21-14:30:11.bin")
    return p.predict(dataframe)
