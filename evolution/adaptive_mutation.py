class AdaptiveMutation:

    @staticmethod
    def stress_multiplier(bacteria):

        multiplier = 1.0

        # ---------- Environmental Stress ----------

        oxygen = bacteria.grn.inputs["oxygen"]

        immune = bacteria.grn.inputs["immune"]

        drug = bacteria.grn.inputs["drug"]

        redox = bacteria.metabolism.redox

        health = bacteria.metabolism.cell_health

        atp = bacteria.metabolism.atp

        if oxygen < 0.30:
            multiplier *= 1.20

        if drug > 0.50:
            multiplier *= 1.30

        if immune > 0.50:
            multiplier *= 1.20

        if atp < 0.20:
            multiplier *= 1.20

        if health < 0.40:
            multiplier *= 1.20

        if redox < 0.30:
            multiplier *= 1.15

        if bacteria.state == bacteria.DORMANT:

            multiplier *= 0.80

        return min(multiplier, 2.0)