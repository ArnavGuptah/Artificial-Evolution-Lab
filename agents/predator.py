import random
import math

from configs.settings import (
    WORLD_WIDTH,
    WORLD_HEIGHT,
    PREDATOR_SPEED,
    PREDATOR_VISION,
    PREDATOR_STARTING_ENERGY,
    PREDATOR_KILL_ENERGY,
    PREDATOR_MAX_AGE,
    PREDATOR_ATTACK_RADIUS,
    PREDATOR_REPRODUCTION_THRESH,
    PREDATOR_REPRODUCTION_COST,
)


class Predator:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.energy = PREDATOR_STARTING_ENERGY
        self.age = 0

    def move(self, organisms):

        nearest_prey = None
        nearest_distance = float("inf")

        for organism in organisms:

            distance = math.hypot(
                self.x - organism.x,
                self.y - organism.y
            )

            if distance < PREDATOR_VISION:

                if distance < nearest_distance:

                    nearest_distance = distance
                    nearest_prey = organism

        if nearest_prey:

            dx = nearest_prey.x - self.x
            dy = nearest_prey.y - self.y

            length = math.hypot(dx, dy)

            if length > 0:

                dx /= length
                dy /= length

        else:

            angle = random.uniform(0, 2 * math.pi)

            dx = math.cos(angle)
            dy = math.sin(angle)

        self.x += dx * PREDATOR_SPEED
        self.y += dy * PREDATOR_SPEED

        self.x = max(0, min(WORLD_WIDTH, self.x))
        self.y = max(0, min(WORLD_HEIGHT, self.y))

        self.energy -= 0.08

    def hunt(self, organisms):

        for organism in organisms[:]:

            distance = math.hypot(
                self.x - organism.x,
                self.y - organism.y
            )

            if distance < PREDATOR_ATTACK_RADIUS:

                organisms.remove(organism)

                self.energy += PREDATOR_KILL_ENERGY

                return

    def update(self, organisms):

        self.move(organisms)

        self.hunt(organisms)

        self.age += 1

        return self.reproduce()

    def is_dead(self):

        return (
            self.energy <= 0
            or self.age >= PREDATOR_MAX_AGE
        )
    
    def reproduce(self):

        if self.energy < PREDATOR_REPRODUCTION_THRESH:
            return None

        self.energy -= PREDATOR_REPRODUCTION_COST

        child = Predator(
            self.x + random.randint(-20, 20),
            self.y + random.randint(-20, 20)
        )

        return child