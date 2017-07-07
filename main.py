import pygame
import sys

from world import World, SingleGenerator, RectGenerator

world = World()

world.add_particles(
    SingleGenerator(100+100j, 1)
)

world.add_particles(
    SingleGenerator(200 + 200j, -2)
)

world.add_particles(
    RectGenerator(
        500 + 500j,
        600 + 550j,
        0.2,
        10
    )
)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    world.step()

    world.draw()
