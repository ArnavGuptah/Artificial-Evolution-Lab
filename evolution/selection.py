from engine.pareto import ParetoOptimizer


class Selection:

    @staticmethod
    def sort(population):

        ParetoOptimizer.rank(population)

        fronts = ParetoOptimizer.fronts(population)

        ordered = []

        for rank in sorted(fronts.keys()):

            front = fronts[rank]

            ParetoOptimizer.crowding_distance(front)

            front.sort(

                key=lambda b: (-b.crowding_distance, -b.fitness)

            )

            ordered.extend(front)

        return ordered