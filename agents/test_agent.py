from core.agent import Agent

from core.action import Action


class TestAgent(Agent):

    def decide(self, environment):

        return Action(

            action_type="HELLO",

            data={

                "message":

                "I am alive"

            }

        )