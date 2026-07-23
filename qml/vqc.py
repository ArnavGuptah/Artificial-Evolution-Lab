import pennylane as qml
import numpy as np
import torch
print(qml.__version__)
print(torch.__version__)
from qml.circuits import variational_circuit, initialize_weights

import torch.nn as nn


class VQC(nn.Module):

    def __init__(self):

        super().__init__()

        self.weights = initialize_weights()

        self.classifier_weights = np.random.randn(8, 4) * 0.1

        self.classifier_bias = np.zeros(4)

        self.optimizer = qml.AdamOptimizer(stepsize=0.02)

    def forward(self, features):

        quantum_output = np.array(

            variational_circuit(features, self.weights)

        )

        logits = (
            quantum_output

            @ self.classifier_weights
            +
            self.classifier_bias
        )

        return logits

    def softmax(self, logits):

        logits = logits - np.max(logits)

        exp = np.exp(logits)

        return exp / np.sum(exp)

    def predict(self, features):

        logits = self.forward(features)

        probabilities = self.softmax(logits)

        return np.argmax(probabilities)

    def loss(self, features, label):

        logits = self.forward(features)

        prediction = self.predict(features)

        return -np.log(probabilities[label] + 1e-9)

    def train(self, X, y, epochs=30):

        for epoch in range(epochs):

            total = 0

            for features, label in zip(X, y):

                self.weights = self.optimizer.step(

                    lambda w:

                    self.loss(features, label),

                    self.weights

                )

                total += self.loss(features, label)

            print(epoch, total / len(X))