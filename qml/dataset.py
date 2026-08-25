import random
from qml.biological_filter import BiologicalFilter
from qml.tasks import PredictionTask

class QuantumDataset:

    def __init__(self, samples):

        self.samples = samples

        self.X = []

        self.y = []

        self.filter = BiologicalFilter()

    def build(self, task=PredictionTask.STATE):

        self.X = []

        self.y = []

        for sample in self.samples:

            filtered = self.filter.select(sample, task)

            features = list(filtered.values())

            self.X.append(features)

            self.y.append(sample["state"])

        return self.X, self.y

    def train_test_split(self, test_ratio=0.2):

        indices = list(range(len(self.X)))

        random.shuffle(indices)

        split = int(len(indices) * (1 - test_ratio))

        train = indices[:split]

        test = indices[split:]

        X_train = [self.X[i] for i in train]

        y_train = [self.y[i] for i in train]

        X_test = [self.X[i] for i in test]

        y_test = [self.y[i] for i in test]

        return (X_train, X_test, y_train, y_test)