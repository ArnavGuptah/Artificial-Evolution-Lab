import math

class NoveltyArchive:

    def __init__(self):

        self.archive = []

    def add(self, bacterium):

        if hasattr(bacterium, "behaviour"):

            self.archive.append(bacterium.behaviour.copy())

        else:

            self.archive.append(bacterium.copy())

    def sample(self):

        return self.archive
    
novelty_archive = NoveltyArchive()

class NoveltySearch:

    @staticmethod
    def distance(a, b):

        behaviour_a = (

            a.behaviour

            if hasattr(a, "behaviour")

            else a

        )

        behaviour_b = (

            b.behaviour

            if hasattr(b, "behaviour")

            else b

        )

        all_keys = set(behaviour_a.keys()) | set(behaviour_b.keys())

        d = 0.0

        for key in behaviour_a:

            value_a = behaviour_a.get(key, 0.0)

            value_b = behaviour_b.get(key, 0.0)

            d += (value_a - value_b) ** 2

        return math.sqrt(d)
    
    @staticmethod
    def score(population, k=5):

        for bacterium in population:

            distances = []

            comparison = population + [
                b for b in novelty_archive.sample()
                if b
            ]

            for other in comparison:

                if other is bacterium:

                    continue

                distances.append(

                    NoveltySearch.distance(bacterium, other))

            distances.sort()

            neighbours = distances[:min(k, len(distances))]

            if neighbours:

                bacterium.novelty = (

                    sum(neighbours)

                    /

                    len(neighbours)

                )

            else:

                bacterium.novelty = 0.0

            if bacterium.novelty > 0.75:

                novelty_archive.add(bacterium)