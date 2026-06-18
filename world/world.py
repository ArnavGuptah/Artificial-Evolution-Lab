import random
import pygame
from core.environment import Environment
from domains.ecology.rules.eat_rule import EatRule

from configs.settings import (
    WORLD_WIDTH,
    WORLD_HEIGHT,
    FPS,
    INITIAL_ORGANISMS,
    INITIAL_FOOD,
    FOOD_SPAWN_RATE,
    MAX_ORGANISMS,
    INITIAL_PREDATORS,
    MAX_PREDATORS,
)

from agents.organism import Organism

from world.renderer import Renderer

from agents.predator import Predator


class World(Environment):

    def __init__(self):
        super().__init__()

        self.rules = []

        self.rules.append(EatRule())

        self.organisms = []

        self.predators = []

        self.food = []

        self.tick = 0
        self.population_history = []
        self.speed_history = []

        self.renderer = Renderer()

        # Spawn organisms
        for _ in range(INITIAL_ORGANISMS):

            organism = Organism(
                random.randint(0, WORLD_WIDTH),
                random.randint(0, WORLD_HEIGHT)
            )

            self.organisms.append(organism)

        #predator spawn
        for _ in range(INITIAL_PREDATORS):

            predator = Predator(
               random.randint(0, WORLD_WIDTH),
               random.randint(0, WORLD_HEIGHT)
            )

            self.predators.append(predator)    

        # Spawn food
        for _ in range(INITIAL_FOOD):

            self.spawn_food()

    def spawn_food(self):

    # Create clustered food zones

        cluster_x = random.randint(50, WORLD_WIDTH - 50)
        cluster_y = random.randint(50, WORLD_HEIGHT - 50)

        cluster_size = random.randint(4, 10)

        for _ in range(cluster_size):

            offset_x = random.randint(-30, 30)
            offset_y = random.randint(-30, 30)

            food_x = cluster_x + offset_x
            food_y = cluster_y + offset_y

            food_x = max(0, min(WORLD_WIDTH, food_x))
            food_y = max(0, min(WORLD_HEIGHT, food_y))

            self.food.append([food_x, food_y])

    def update(self):
        self.actions = []

        for organism in self.organisms:

            action = organism.decide(self)

            if action:

                self.actions.append(

                    (

                    organism,

                    action

                    )

                )

        self.tick += 1

        new_predators = []

        for predator in self.predators:

            child = predator.update(self.organisms)

            if child:
                new_predators.append(child)

        if len(self.predators) < MAX_PREDATORS:

            self.predators.extend(new_predators)

        # Random food spawning
        if len(self.food) < 250:

            if random.random() < FOOD_SPAWN_RATE:
                self.spawn_food()

        new_organisms = []
        child = None

        for organism in self.organisms:

          child = organism.update(
             self.food,
             self.organisms
          )

          if child and len(self.organisms) < MAX_ORGANISMS:
           new_organisms.append(child)

        self.organisms.extend(new_organisms)

        # Remove dead organisms
        self.organisms = [
            organism
            for organism in self.organisms
            if not organism.is_dead()
        ]

        self.predators = [
            predator
            for predator in self.predators
            if not predator.is_dead()
        ]

        for rule in self.rules:

            rule.apply(self)

        if self.tick % 100 == 0:

            self.population_history.append(
               len(self.organisms)
            )

            if len(self.organisms) > 0:

                avg_speed = sum(
                    org.genome["speed"]
                    for org in self.organisms
                ) / len(self.organisms)

            else:

                avg_speed = 0

            self.speed_history.append(avg_speed)

            print(
            f"Tick: {self.tick} | "
            f"Population: {len(self.organisms)} | "
            f"Predators: {len(self.predators)} |"
            f"Avg Speed: {avg_speed:.2f}"
            )


    def run(self):

        clock = pygame.time.Clock()

        running = True

        while running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

            self.update()

            self.renderer.draw(
                self.organisms,
                self.predators,
                self.food,
                self.tick
            )

            clock.tick(FPS)

        pygame.quit()