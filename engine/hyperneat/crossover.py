class CPPNCrossover:

    @staticmethod
    def crossover(parent1, parent2):

        child_cppn = CPPNCrossover.crossover(

            parent1.genome["cppn"],
            parent2.genome["cppn"]

        )
