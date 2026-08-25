from qml.dataset import QuantumDataset
from qml.qsvm import QSVM


class QSVMTrainer:

    def __init__(self, samples):

        self.dataset = QuantumDataset(samples)

        self.model = QSVM()

    def train(self):

        X, y = self.dataset.build()

        self.dataset.build()

        X_train, X_test, y_train, y_test = (

            self.dataset.train_test_split()

        )

        self.model.fit(X_train, y_train)

        accuracy = self.model.evaluate(X_test, y_test, X_train)

        print()

        print("========== QSVM RESULTS ==========")

        print(f"Accuracy : {accuracy:.4f}")

        self.model.save()

        print("Model saved as qsvm.pkl")

        return accuracy