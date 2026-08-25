import os
from qml.qsvm import QSVM


class QuantumInference:

    def __init__(self, config=None, backend="qsvm"):

        self.model = None

        self.loaded = False

        if os.path.exists("qsvm.pkl"):

            backend = "qsvm"

            if config is not None:

                backend = config["qml"]["backend"]

                if backend == "qsvm":

                    self.model = QSVM()

                else:

                    raise ValueError(f"Unknown QML backend: {backend}")

            self.model.load("qsvm.pkl")

            self.loaded = True

            print("Quantum model loaded (QSVM).")

        else:

            print("No trained QSVM found.")

    def available(self):

        return self.loaded

    def predict(self, sample, X_train):

        if not self.loaded:

            return None

        if len(X_train) == 0:

            return None

        return self.model.predict_probability(sample, X_train)