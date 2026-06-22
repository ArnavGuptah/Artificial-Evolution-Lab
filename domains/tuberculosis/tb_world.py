import random
import math
import pygame
from domains.tuberculosis.granuloma import Granuloma
from domains.tuberculosis.immune_cell import ImmuneCell
from domains.tuberculosis.oxygen_field import OxygenField
from configs.settings import (

    WORLD_WIDTH,

    WORLD_HEIGHT,

    FPS

)

from domains.tuberculosis.macrophage import Macrophage
from domains.tuberculosis.bacteria import Bacteria
from domains.tuberculosis.tb_renderer import TBRenderer


class TBWorld:


    def __init__(self):


        self.tick = 0


        self.antibiotics = False


        self.bacteria = []

        self.granulomas = []

        self.renderer = TBRenderer()

        self.immune_cells = []

        self.oxygen = OxygenField(WORLD_WIDTH, WORLD_HEIGHT)

        for _ in range(40):

                self.immune_cells.append(

                    ImmuneCell(

                        random.randint(0, WORLD_WIDTH),

                        random.randint( 0, WORLD_HEIGHT )
                        
                    )

                )

        self.immune_cells = []

        for _ in range(40):

            cell = ImmuneCell(

                random.randint(0,WORLD_WIDTH),

                random.randint(0,WORLD_HEIGHT)

            )

            self.immune_cells.append(cell)

        for _ in range(200):


            b = Bacteria(

                random.randint(

                    0,

                    WORLD_WIDTH

                ),

                random.randint(

                    0,

                    WORLD_HEIGHT

                )

            )

            self.bacteria.append(b)

        self.macrophages = []


        for _ in range(60):

            self.macrophages.append(

                Macrophage(

                    random.randint(

                        0,

                        WORLD_WIDTH

                    ),

                    random.randint(

                        0,

                        WORLD_HEIGHT

                    )

                )
            )



    def update(self):

        self.oxygen.grid[:] = 1.0
        self.tick += 1
        self.update_oxygen()

        # Macrophage <-> TB interaction

        for m in self.macrophages:

            for b in self.bacteria[:]:

                if b.state == Bacteria.DEAD:

                    continue

                if m.state != Macrophage.HEALTHY:

                    continue

                d = math.hypot(

                b.x - m.x,

                b.y - m.y

                )

                if d < 8:

                    m.infect()

                    b.state = Bacteria.DEAD

                    break

        if self.tick == 2000:

            self.antibiotics = True

        if self.tick == 5000:

            self.antibiotics = False


        newborns = []

        for b in self.bacteria:

            b.update(self.oxygen)

            if self.antibiotics:

                if b.state == "ACTIVE":

                    kill_prob = (1 - b.genome["drug_resistance"])


                    if random.random() < kill_prob * 0.02:

                        b.state = "DEAD"


            if b.state == Bacteria.DEAD:

                continue

            child = b.reproduce()


            if child:

                newborns.append(

                    child

                )


            if self.antibiotics:


                if (

                    b.state

                    ==

                    Bacteria.ACTIVE

                ):


                    kill_prob = (

                        1

                        -

                        b.genome[

                            "drug_resistance"

                        ]

                    )


                    if (

                        random.random()

                        <

                        kill_prob * 0.02

                    ):


                        b.state = (

                            Bacteria.DEAD

                        )


        self.bacteria.extend(

            newborns

        )

        new_bacteria = []

        for m in self.macrophages:

            burst = m.update()

            if burst:

                for _ in range(

                    m.intracellular_tb

                ):

                    child = Bacteria(

                        m.x +

                        random.randint(

                            -20,

                            20

                        ),

                        m.y +

                        random.randint(

                            -20,

                            20

                        )

                    )

                    new_bacteria.append(child)

        self.bacteria.extend(new_bacteria)

        self.bacteria = [

            b

            for b in self.bacteria

            if b.state

            !=

            Bacteria.DEAD

        ]

        self.macrophages = [

            m

            for m in self.macrophages

            if m.state != Macrophage.DEAD

        ]


        if self.tick % 100 == 0:

            active = sum(

                1

                for b in self.bacteria

                if b.state == "ACTIVE"

            )


            dormant = sum(

                1

                for b in self.bacteria

                if b.state == "DORMANT"

            )


            resistant = sum(

                1

                for b in self.bacteria

                if b.genome["drug_resistance"] > 0.7

            )


            print(

                f"Tick:{self.tick}"

                f" | Pop:{len(self.bacteria)}"

                f" | Active:{active}"

                f" | Dormant:{dormant}"

                f" | Resistant:{resistant}"

            )

            resistant = sum(

                1

                for b in self.bacteria

                if

                b.genome[ "drug_resistance"] > 0.6

            )


            print(

                f"Tick : {self.tick}"

                f" | Population : {len(self.bacteria)}"

                f" | Resistant : {resistant}"

            )

        if self.tick % 200 == 0:

            for m in self.macrophages:

                if m.state != Macrophage.INFECTED:

                    continue


                nearby_immune = 0


                for immune in self.immune_cells:

                    d = math.hypot(

                        immune.x - m.x,

                        immune.y - m.y

                    )


                    if d < 60:

                        nearby_immune += 1


                if nearby_immune > 15:

                    already_exists = False


                    for g in self.granulomas:

                        d = math.hypot(

                            m.x - g.x,

                            m.y - g.y

                        )


                        if d < g.radius:

                            already_exists = True

                            break


                    if not already_exists:

                        self.granulomas.append(

                            Granuloma(

                                m.x,

                                m.y,

                                50

                            )

                        )

        for immune in self.immune_cells:

            strongest = None

            signal = 0


            for m in self.macrophages:

                if m.signal_strength > signal:

                    signal = m.signal_strength

                    strongest = m


            if strongest:

                immune.move_towards(

                    strongest.x,

                    strongest.y

                )

    def run(self):


        clock = pygame.time.Clock()


        running = True


        while running:


            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_o:

                        self.renderer.show_oxygen = (

                            not self.renderer.show_oxygen

                        )

                if (event.type == pygame.QUIT ):

                    running = False


            self.update()


            self.renderer.draw(

                self.bacteria,
                self.granulomas,
                self.tick,
                self.immune_cells,
                self.antibiotics,
                self.oxygen,
                self.macrophages
            )


            clock.tick(

                FPS

            )


        pygame.quit()

    def update_oxygen(self):

        self.oxygen.grid[:] = 1.0

        for g in self.granulomas:

            for row in range(self.oxygen.rows):

                for col in range(self.oxygen.cols):

                    x = col * self.oxygen.resolution

                    y = row * self.oxygen.resolution

                    d = math.hypot(

                        x - g.x,

                        y - g.y

                    )

                    if d < g.radius:

                        factor = d / g.radius

                        oxygen = 0.1 + 0.9 * factor

                        self.oxygen.grid[row,col] = min(

                            self.oxygen.grid[row,col],

                            oxygen

                        )