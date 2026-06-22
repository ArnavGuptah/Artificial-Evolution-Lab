import pygame

from configs.settings import (

    WORLD_WIDTH,

    WORLD_HEIGHT

)

from domains.tuberculosis.bacteria import Bacteria
from domains.tuberculosis.macrophage import Macrophage


class TBRenderer:


    def __init__(self):

        pygame.init()
        self.show_oxygen = False

        self.screen = pygame.display.set_mode(

            (

                WORLD_WIDTH,

                WORLD_HEIGHT

            )

        )


        pygame.display.set_caption(

            "TB Evolution Simulator"

        )


        self.font = pygame.font.SysFont("consolas", 20)


    def draw( self, bacteria, granulomas, tick, immune_cells ,antibiotics, oxygen, macrophages):


        self.screen.fill((10,10,10))
        if self.show_oxygen:

            self.draw_oxygen(

                oxygen

            )

        for b in bacteria:


            if b.state == Bacteria.DEAD:

                continue

            colour = b.lineage_color

            pygame.draw.circle(

                self.screen,

                color,

                (

                    int(b.x),

                    int(b.y)

                ),

                3

            )

        for g in granulomas:

            pygame.draw.circle(

                self.screen,

                (150,150,150),

                (

                    int(g.x),

                    int(g.y)

                ),

                g.radius,

                2

            )

        for immune in immune_cells:

            pygame.draw.circle(

                self.screen,

                (0,100,255),

                (

                    int(immune.x),

                    int(immune.y)

                ),

                4

            )

        text = self.font.render(

            f"Tick : {tick}",

            True,

            (255,255,255)

        )


        self.screen.blit(

            text,

            (20,20)

        )


        if antibiotics:


            txt = self.font.render(

                "ANTIBIOTICS ACTIVE",

                True,

                (255,100,100)

            )


            self.screen.blit(

                txt,

                (20,50)

            )

        for m in macrophages:

            if m.state == Macrophage.HEALTHY:

                color = (0,150,255)

            else:

                color = (255,0,255)

            pygame.draw.circle(self.screen, color, (int(m.x), int(m.y)), 6)


        pygame.display.flip()


    def draw_oxygen(self, oxygen):

        cell = oxygen.resolution


        for row in range(oxygen.rows):

            for col in range(oxygen.cols):

                value = oxygen.grid[row,col]


                intensity = int(value * 255)


                color = (intensity, intensity, intensity)


                pygame.draw.rect(self.screen, color, (

                    col * cell,

                    row * cell,

                    cell,

                    cell

                    )

                )

