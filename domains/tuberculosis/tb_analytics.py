#we're separating Simulation from Analysis
class TBAnalytics:

    FEATURE_ORDER = [

        "dosR",
        "sigH",
        "sigE",
        "growth",
        "atp",
        "redox",
        "health",
        "oxygen",
        "energy",
        "fitness"

    ]

    def __init__(self):

        self.history = {

            "population": [],

            "avg_dosR": [],

            "avg_sigH": [],

            "avg_sigE": [],

            "avg_growth": [],

            "avg_atp": [],

            "avg_redox": [],

            "avg_health": [],

            "avg_quantum_confidence": [],

            "avg_quantum_bonus": [],

        }

        self.samples = []

    def record(self, world):

        bacteria = world.bacteria

        if len(bacteria) == 0:

            return

        N = len(bacteria)

        quantum_confidence = 0.0

        quantum_bonus = 0.0

        self.history["population"].append(N)

        self.history["avg_dosR"].append(

            sum(
                b.grn.regulators["dosR"]
                for b in bacteria
            ) / N
        )

        self.history["avg_sigH"].append(

            sum(
                b.grn.regulators["sigH"]
                for b in bacteria
            ) / N
        )

        self.history["avg_sigE"].append(

            sum(
                b.grn.regulators["sigE"]
                for b in bacteria
            ) / N
        )

        self.history["avg_growth"].append(

            sum(
                b.grn.functions["growth"]
                for b in bacteria
            ) / N
        )

        self.history["avg_atp"].append(

            sum(
                b.metabolism.atp
                for b in bacteria
            ) / N
        )

        self.history["avg_redox"].append(

            sum(
                b.metabolism.redox
                for b in bacteria
            ) / N
        )

        self.history["avg_health"].append(

            sum(
                b.metabolism.cell_health
                for b in bacteria
            ) / N
        )

        for b in bacteria:

            if b.quantum_prediction is not None:

                quantum_confidence += max(

                    b.quantum_prediction

                )

                quantum_bonus += 0.05 * max(

                    b.quantum_prediction

                )

        self.history["avg_quantum_confidence"].append(

            quantum_confidence / N

        )

        self.history["avg_quantum_bonus"].append(

            quantum_bonus / N

        )

        for b in bacteria:

            self.samples.append({

                "dosR": b.grn.regulators["dosR"],

                "sigH": b.grn.regulators["sigH"],

                "sigE": b.grn.regulators["sigE"],

                "growth": b.grn.functions["growth"],

                "atp": b.metabolism.atp,

                "redox": b.metabolism.redox,

                "health": b.metabolism.cell_health,

                "oxygen": b.metabolism.oxygen,

                "energy": b.energy,

                "fitness": b.fitness,

                "generation": b.generation,

                "state": b.state

            })

    def dataset(self):

        X = []

        y = []

        for sample in self.samples:

            X.append([

                sample[name]
                for name in self.FEATURE_ORDER

            ])

            y.append(sample["state"])

        return X, y