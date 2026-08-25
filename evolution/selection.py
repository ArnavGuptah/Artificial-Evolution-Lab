from engine.pareto import ParetoOptimizer


class Selection:

    @staticmethod
    def sort(population):

        best = max(
            population,
            key=lambda b: b.fitness,
            default=None
        )

        ParetoOptimizer.rank(population)

        fronts = ParetoOptimizer.fronts(population)

        ordered = []

        for rank in sorted(fronts.keys()):

            front = fronts[rank]

            ParetoOptimizer.crowding_distance(front)

            front.sort(

                key=lambda b: (-b.crowding_distance, -b.novelty, -b.fitness)

            )

            ordered.extend(front)

        if best is not None:

            ordered = [b for b in ordered if b != best]

            ordered.insert(0, best)

        return ordered