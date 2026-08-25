from qml.tasks import PredictionTask

class BiologicalFilter:

    def __init__(self):

        self.feature_sets = {

            PredictionTask.STATE: [

                "atp",
                "growth",
                "dosR",
                "sigH",
                "oxygen",
                "health",
                "energy",
                "fitness"

            ]

        }

    def select(self, sample, task=PredictionTask.STATE):

        selected = {}

        for feature in self.feature_sets[task]:

            selected[feature] = sample[feature]

        return selected