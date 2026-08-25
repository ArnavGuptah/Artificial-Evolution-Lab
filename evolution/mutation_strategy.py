from abc import ABC, abstractmethod

class MutationStrategy(ABC):

    @abstractmethod
    def mutate_genome(self, genome, bounds):
        pass

    @abstractmethod
    def mutate_cppn(self, cppn, speciation, stress, parent):
        pass