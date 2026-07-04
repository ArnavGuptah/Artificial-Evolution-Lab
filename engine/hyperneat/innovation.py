class InnovationTracker:

    def __init__(self):

        self.counter = 0

        self.history = {}

    def connection_id(self, source, target):

        key = (source, target)

        if key not in self.history:

            self.counter += 1

            self.history[key] = self.counter

        return self.history[key]

    def total_connections(self):

        return self.counter
    
innovation_tracker = InnovationTracker()
