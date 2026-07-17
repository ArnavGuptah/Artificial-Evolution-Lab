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

        self.compatibility_threshold = 1.0

        self.target_species = 20

    def distance(self, cppn1, cppn2):

        diff = 0.0
        count = 0

        for row1, row2 in zip(cppn1.w1, cppn2.w1):

            for a, b in zip(row1, row2):

                diff += abs(a - b)
                count += 1

        for a, b in zip(cppn1.w2, cppn2.w2):

            diff += abs(a - b)
            count += 1

        if count == 0:
            return 0.0

        return diff / count
        
    def assign(self, cppn):

        for species in self.species:

            if species.representative is None:
                continue

            d = self.distance(

                cppn,
                species.representative
            )

            print(
                f"[Species] "
                f"distance={d:.3f} "
                f"threshold={self.compatibility_threshold:.3f}"
            )

            if d < self.compatibility_threshold:

                cppn.species_id = species.id

                species.add(cppn)

                return species.id

        new_species = CPPNSpecies(

            len(self.species)

        )

        cppn.species_id = new_species.id

        new_species.add(cppn)

        self.species.append(new_species)

        return new_species.id
    
    def clear(self):

        survivors = []

        for species in self.species:

            species.update_representative()
            species.update_progress()
            species.members.clear()

            if species.stagnation < 20:
                survivors.append(species)

        self.species = survivors

        self.species = [
        s
        for s in self.species
        if s.representative is not None
    ]

    def mutation_rate(self, cppn):

        species = None

        for s in self.species:

            if s.id == cppn.species_id:

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

        if species.stagnation > 10:

            mutation_rate *= 1.5
            sigma *= 1.5

        mutation_rate = min(mutation_rate, 0.40)
        sigma = min(sigma, 0.50)

        return mutation_rate, sigma

    def adapt_threshold(self):

        count = len(self.species)

        if count > self.target_species:

            self.compatibility_threshold += 0.01

        elif count < self.target_species:

            self.compatibility_threshold -= 0.01

        self.compatibility_threshold = max(
            0.15,
            min(1.0, self.compatibility_threshold)
        )