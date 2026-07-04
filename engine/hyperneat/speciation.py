import math


class CPPNSpecies:

    def __init__(self, species_id):

        self.id = species_id

        self.members = []

        self.representative = None

        self.best_fitness = 0.0

        self.stagnation = 0

    def add(self, cppn):

        self.members.append(cppn)

        if self.representative is None:

            self.representative = cppn

    def update_representative(self):

        if not self.members:
            return

        self.representative = max(
            self.members,
            key=lambda cppn: cppn.fitness
        )

    def average_fitness(self):

        if not self.members:

            return 0.0

        return (

            sum(cppn.fitness for cppn in self.members)

            / len(self.members)

        )
    
    def update_progress(self):

        current = self.average_fitness()

        if current > self.best_fitness:

            self.best_fitness = current

            self.stagnation = 0

        else:

            self.stagnation += 1

class SpeciationManager:

    def __init__(self):

        self.species = []

        self.compatibility_threshold = 2.5

    def distance(self, cppn1, cppn2):

        d = 0.0

        for row1, row2 in zip(cppn1.w1, cppn2.w1):

            for a, b in zip(row1, row2):

                d += abs(a - b)

        for a, b in zip(cppn1.w2, cppn2.w2):

            d += abs(a - b)

        return d
        
    def assign(self, cppn):

        for species in self.species:

            d = self.distance(

                cppn,
                species.representative
            )

            if d < self.compatibility_threshold:

                cppn.species_id = species.id

                species.add(cppn)

                return species.id

        new_species = CPPNSpecies(

            len(self.species)

        )

        new_species.add(cppn)

        self.species.append(new_species)

        return new_species.id
    
    def clear(self):

        for species in self.species:

            species.update_representative()

            species.members.clear()

    def mutation_rate(self, cppn):

        species = None

        for s in self.species:

            if cppn in s.members:

                species = s

                break

        if species is None:

            return 0.10, 0.20

        fitness = species.average_fitness()

        mutation_rate = 0.10

        sigma = 0.20

        if fitness > 18:

            mutation_rate = 0.05
            sigma = 0.10

        elif fitness > 10:

            mutation_rate = 0.10
            sigma = 0.20

        else:

            mutation_rate = 0.18
            sigma = 0.35

        # ---- Species has stopped improving ----

        if species.stagnation > 10:

            mutation_rate *= 1.5
            sigma *= 1.5

        mutation_rate = min(mutation_rate, 0.40)
        sigma = min(sigma, 0.50)

        return mutation_rate, sigma