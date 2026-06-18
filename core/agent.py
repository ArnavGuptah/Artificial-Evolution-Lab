from core.action import Action


class Agent:

    def __init__(self):

        self.traits = {}

        self.state = {}

    def perceive(self, environment):

        pass

    def decide(self, environment):

        return None

    def update(self, environment):

        return self.decide(environment)