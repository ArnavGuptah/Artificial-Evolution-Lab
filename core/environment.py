class Environment:

    def __init__(self):

        self.agents = []

        self.resources = []

        self.tick = 0

    def update(self):

        self.tick += 1