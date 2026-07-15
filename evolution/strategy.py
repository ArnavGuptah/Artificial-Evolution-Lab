from abc import ABC, abstractmethod


class EvolutionStrategy(ABC):
    """
    Defines how one evolutionary generation is produced.
    """

    @abstractmethod
    def evolve(self, world):
        """
        Perform one evolutionary step.

        Parameters
        ----------
        world : TBWorld
            Current simulation world.
        """
        pass