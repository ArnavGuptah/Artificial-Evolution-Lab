from core.rule import Rule

import math

from configs.settings import (

    FOOD_RADIUS,

    FOOD_ENERGY

)


class EatRule(Rule):

    def apply(self, environment):

        for organism in environment.organisms:

            for food in environment.food[:]:

                distance = math.hypot(

                    organism.x - food[0],

                    organism.y - food[1]

                )

                if distance < FOOD_RADIUS:

                    organism.energy += FOOD_ENERGY

                    if organism.energy > 400:

                        organism.energy = 400

                    environment.food.remove(food)

                    break