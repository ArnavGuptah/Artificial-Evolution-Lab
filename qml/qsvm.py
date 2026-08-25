from sklearn.svm import SVC
from qml.kernel import QuantumKernel
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

class QSVM:

    def __init__(self):

        self.kernel = QuantumKernel()

        self.model = SVC(kernel="precomputed", probability=True)

    def fit(self, X_train, y_train):

        K = self.kernel.train_kernel(X_train)

        self.model.fit(K, y_train)

    def predict(self, X_test, X_train):

        K = self.kernel.predict_kernel(X_test, X_train)

        return self.model.predict(K)

    def predict_single(self, sample, X_train):

        prediction = self.predict([sample], X_train)

        return prediction[0]

    def predict_probability(self, sample, X_train):

        K = self.kernel.predict_kernel([sample], X_train)

        probabilities = self.model.predict_proba(K)[0]

        return probabilities

    def evaluate(self, X_test, y_test, X_train):

        predictions = self.predict(X_test, X_train)

        accuracy = accuracy_score(y_test, predictions)

        return accuracy

    def evaluate(self, X_test, y_test, X_train):

        predictions = self.predict(X_test, X_train)

        accuracy = accuracy_score(y_test, predictions)

        matrix = confusion_matrix(y_test, predictions)

        report = classification_report(y_test, predictions)

        print()

        print("========== CONFUSION MATRIX ==========")

        print(matrix)

        print()

        print("========== CLASSIFICATION REPORT ==========")

        print(report)

        return accuracy

    def save(self, filename="qsvm.pkl"):

        joblib.dump(self.model, filename)

    def load(self, filename="qsvm.pkl"):

        self.model = joblib.load(filename)

    