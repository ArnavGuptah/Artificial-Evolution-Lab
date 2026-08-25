from enum import Enum
#if you mistype any task, your IDE and Python will catch it much earlier.

class PredictionTask(Enum):

    STATE = "state_prediction"

    DRUG_RESISTANCE = "drug_resistance"

    SURVIVAL = "survival"

    FITNESS = "fitness"

    SPECIES = "species"

    TREATMENT_OUTCOME = "treatment_outcome"