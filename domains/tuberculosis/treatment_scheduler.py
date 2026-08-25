class TreatmentScheduler:

    def __init__(self):

        self.schedule = [

            (0, {
                "INH": False,
                "RIF": False,
                "PZA": False,
                "EMB": False
            }),

            (2000, {
                "INH": True,
                "RIF": False,
                "PZA": False,
                "EMB": False
            }),

            (4000, {
                "INH": True,
                "RIF": True,
                "PZA": False,
                "EMB": False
            }),

            (7000, {
                "INH": True,
                "RIF": True,
                "PZA": True,
                "EMB": True
            })
        ]

    def current(self, tick):

        treatment = self.schedule[0][1]

        for t, drugs in self.schedule:

            if tick >= t:

                treatment = drugs

            else:

                break

        return treatment