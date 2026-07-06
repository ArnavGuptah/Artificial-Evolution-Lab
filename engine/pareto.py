class ParetoOptimizer:

    @staticmethod
    def dominates(a, b):

        better_or_equal = True

        strictly_better = False

        objectives_a = getattr(a, "objectives", {})
        objectives_b = getattr(b, "objectives", {})

        for key in objectives_a:

            if objectives_a[key] < objectives_b[key]:

                better_or_equal = False

                break

            elif objectives_a[key] > objectives_b[key]:

                strictly_better = True

        return better_or_equal and strictly_better

    @staticmethod
    def rank(population):

        for bacterium in population:

            bacterium.pareto_rank = 0

        for bacterium in population:

            dominated_by = 0

            for other in population:

                if other is bacterium:

                    continue

                if ParetoOptimizer.dominates(other, bacterium):

                    dominated_by += 1

            bacterium.pareto_rank = dominated_by

    @staticmethod
    def fronts(population):

        fronts = {}

        for bacterium in population:

            rank = bacterium.pareto_rank

            if rank not in fronts:

                fronts[rank] = []

            fronts[rank].append(bacterium)

        return fronts
    
    @staticmethod
    def crowding_distance(front):

        if len(front) <= 2:

            for bacterium in front:

                bacterium.crowding_distance = float("inf")

            return

        for bacterium in front:

            bacterium.crowding_distance = 0.0

        objectives = list(front[0].objectives.keys())

        for objective in objectives:

            front.sort(

                key=lambda b: b.objectives[objective]

            )

            front[0].crowding_distance = float("inf")

            front[-1].crowding_distance = float("inf")

            minimum = front[0].objectives[objective]

            maximum = front[-1].objectives[objective]

            if maximum == minimum:

                continue

            for i in range(1, len(front)-1):

                previous = front[i-1].objectives[objective]

                next_value = front[i+1].objectives[objective]

                front[i].crowding_distance += (

                    (next_value - previous)

                    /

                    (maximum - minimum)

                )