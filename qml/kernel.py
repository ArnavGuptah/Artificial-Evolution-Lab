import pennylane as qml
import numpy as np

from qml.circuits import (
    embedding_circuit,
    initialize_weights

)

class QuantumKernel:

    def __init__(self):

        self.weights = initialize_weights()

        print("Quantum kernel initialized")

    def similarity(self, x1, x2):

        psi1 = embedding_circuit(x1, self.weights)

        psi2 = embedding_circuit(x2, self.weights)

        overlap = np.vdot(psi1, psi2)

        fidelity = np.abs(overlap) ** 2

        return float(fidelity)

    def kernel_matrix(self, X):

        n = len(X)

        K = np.zeros((n, n))

        for i in range(n):

            for j in range(n):

                K[i, j] = self.similarity(

                    X[i],

                    X[j]

                )

        return K

    def train_kernel(self, X_train):

        return self.kernel_matrix(X_train)

    def predict_kernel(self, X_test, X_train):

        rows = len(X_test)

        cols = len(X_train)

        K = np.zeros((rows, cols))

        for i in range(rows):

            for j in range(cols):

                K[i, j] = self.similarity(

                    X_test[i],

                    X_train[j]

                )

        return K