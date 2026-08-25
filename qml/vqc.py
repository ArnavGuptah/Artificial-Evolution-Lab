import torch
import torch.nn as nn
import torch.optim as optim
import pennylane as qml

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)

from qml.circuits import (
    N_QUBITS,
    N_LAYERS,
    vqc_circuit
)

class VQC:

    def __init__(self):

        self.model = QuantumNet(self.n_classes)
        self.label_map = {}
        self.inverse_label_map = {}
        self.n_classes = 5
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.criterion = nn.CrossEntropyLoss()

    def encode_labels(self, labels):

        unique = sorted(set(labels))

        self.label_map = {
            label: i
            for i, label in enumerate(unique)
        }

        self.inverse_label_map = {
            i: label
            for label, i in self.label_map.items()
        }

        return [
            self.label_map[y]
            for y in labels
        ]

    def decode_predictions(self, predictions):

        return [
            self.inverse_label_map[p]
            for p in predictions
        ]

    def fit(self, X_train, y_train, epochs=25):

        y_train = self.encode_labels(y_train)

        X = torch.tensor(X_train, dtype=torch.float32)

        y = torch.tensor(y_train, dtype=torch.long)

        self.model.train()

        for epoch in range(epochs):

            self.optimizer.zero_grad()

            logits = self.model(X)

            loss = self.criterion(logits, y)

            loss.backward()

            self.optimizer.step()

            print(
                f"Epoch {epoch+1}/{epochs}"
                f"  Loss={loss.item():.4f}"
            )

    def predict(self, X):
    
        self.model.eval()

        X = torch.tensor(X, dtype=torch.float32)

        with torch.no_grad():

            logits = self.model(X)

            predictions = torch.argmax(logits, dim=1)

        predictions = predictions.cpu().numpy()

        return self.decode_predictions(predictions)

    def predict_single(self, sample):

        return self.predict([sample])[0]

    def predict_probability(self, sample):

        self.model.eval()

        X = torch.tensor([sample], dtype=torch.float32)

        with torch.no_grad():

            logits = self.model(X)

            probabilities = torch.softmax(logits, dim=1)

        return probabilities[0].cpu().numpy()

    def evaluate(self, X_test, y_test):

        predictions = self.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)

        matrix = confusion_matrix(y_test, predictions)

        report = classification_report(y_test, predictions)

        print()

        print("========== VQC RESULTS ==========")

        print(f"Accuracy : {accuracy:.4f}")

        print()

        print("========== CONFUSION MATRIX ==========")

        print(matrix)

        print()

        print("========== CLASSIFICATION REPORT ==========")

        print(report)

        return accuracy

    def save(self, filename="vqc.pt"):

        torch.save(

            {
                "model": self.model.state_dict(),
                "label_map": self.label_map
            },

            filename

        )

    def load(self, filename="vqc.pt"):

        checkpoint = torch.load(filename, map_location="cpu")

        self.model.load_state_dict(checkpoint["model"])

        self.label_map = checkpoint["label_map"]

        self.inverse_label_map = {

            v: k
            for k, v in self.label_map.items()

        }

        self.model.eval()

class QuantumNet(nn.Module):

    def __init__(self, n_classes):

        super().__init__()

        weight_shapes = {

            "weights": (N_LAYERS, N_QUBITS)

        }

        self.quantum = qml.qnn.TorchLayer(vqc_circuit, weight_shapes)

        self.classifier = nn.Sequential(

            nn.Linear(N_QUBITS, 32),

            nn.ReLU(),

            nn.Linear(32, n_classes)

        )

        

    def forward(self, x):

        x = self.quantum(x)
        x = self.classifier(x)
        return x

    