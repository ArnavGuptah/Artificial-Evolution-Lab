from evolution.strategy import EvolutionStrategy
from evolution.selection import Selection

class ClassicalStrategy(EvolutionStrategy):

    def evolve(self, world):
        
        world.perform_reproduction()

        world.perform_selection()

        world.perform_speciation()