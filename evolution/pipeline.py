from abc import ABC, abstractmethod

class EvolutionPipeline(ABC):
    #Coordinates one evolutionary step.
    #Biology stays outside this class.

    @abstractmethod
    def evolve(self, world):
        #Perform one evolutionary cycle.
        pass