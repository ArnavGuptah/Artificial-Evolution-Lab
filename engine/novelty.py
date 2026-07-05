import math


class NoveltySearch:

    @staticmethod
    def distance(a, b):

        d = 0.0

        for key in a.behaviour:

            d += (

                a.behaviour[key]

                -

                b.behaviour[key]

            ) ** 2

        return math.sqrt(d)
    
    @staticmethod
    def score(population, k=5):

        for bacterium in population:

            distances = []

            comparison = population + novelty_archive.sample()

            for other in comparison:

                if other is bacterium:

                    continue

                distances.append(

                    NoveltySearch.distance(

                        bacterium,

                        other

                    )

                )

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

class NoveltyArchive:

    def __init__(self):

        self.archive = []

    def add(self, bacterium):

        self.archive.append(bacterium)

    def sample(self):

        return self.archive