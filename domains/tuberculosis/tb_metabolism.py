import random

class TBMetabolism:

    def __init__(self):

        self.atp = 1.0

        self.redox = 0.5

        self.cell_health = 1.0

    def update(self, grn, inputs):

    # ---------- ATP ----------

        production = (
            0.20
            * (inputs["oxygen"] ** 2)
            * grn.physiology["metabolism"]
        )

        maintenance = 0.03

        growth_cost = (
            0.05
            * grn.functions["growth"]
        )

        stress_cost = (
            0.02 * grn.regulators["sigH"]
            + 0.02 * grn.regulators["sigE"]
            + 0.05 * inputs["immune"]
        )

        target_atp = (
            0.15
            + 0.75 * inputs["oxygen"]
        )

        self.atp += (
            0.08 * (target_atp - self.atp)
        )

        self.atp -= (
            0.02 * grn.functions["growth"]
        )

        self.atp -= (
            0.015 * inputs["immune"]
        )

        self.atp -= (
            0.015 * inputs["drug"]
        )

        self.atp = max(0.05, min(1.0, self.atp))

        self.atp = max(0.0, min(1.0, self.atp))

        if inputs["oxygen"] < 0.30:

            print(
                f"[ATP] "
                f"O2={inputs['oxygen']:.2f} "
                f"ATP={self.atp:.2f}"
            )

        # ---------- Redox ----------

        oxidative_stress = (
            0.5 * inputs["immune"]
            + 0.5 * inputs["drug"]
        )

        self.redox += (

            0.05 * grn.regulators["whiB3"]

            - 0.02 * oxidative_stress

        )

        self.redox = max(
            0.0,
            min(1.0, self.redox)
        )

        grn.inputs["redox"] = self.redox

        damage = (
            0.04 * inputs["drug"]
            +
            0.06 * inputs["immune"]
        )

        repair = (
            0.03 * self.atp
        )

        self.cell_health += (
            repair
            - damage
        )

        self.cell_health = max(
            0.0,
            min(1.0, self.cell_health)
        )