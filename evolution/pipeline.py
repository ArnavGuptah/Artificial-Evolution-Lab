class EvolutionPipeline:
    #Coordinates one evolutionary step.
    #Biology stays outside this class.

    def __init__(self, strategy):

        self.strategy = strategy
    
    def evolve(self, world):
        
        self.strategy.evolve(world)