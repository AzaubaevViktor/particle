import pygame
import sys

from world import World, SingleGenerator, RectGenerator, Circle4Generator

world = World(
    friction=0
)

world.add_particles(
    SingleGenerator(100+100j, 1)
)

world.add_particles(
    SingleGenerator(200 + 200j, -2)
)

if False:
    world.add_particles(
        Circle4Generator(
            500 + 500j,
            10,
            0.5,
            30
        )
    )

    world.add_particles(
        Circle4Generator(
            700 + 500j,
            10,
            0.8,
            -30
        )
    )

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    world.step()

    world.draw()
