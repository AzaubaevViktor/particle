import sys
import time
import pygame

from world import World, SingleGenerator, RectGenerator, Circle4Generator, \
    Circle6Generator, Rect6Generator

world = World(
    friction=0.1,
    dT=0.01,
    draw_k=2,
)

world.add_particles(
    SingleGenerator(500+100j, 1)
)

world.add_particles(
    SingleGenerator(500 + 200j, -2)
)


world.add_particles(
    Circle6Generator(
        200 + 200j,
        15,
        0.4,
        0
    )
)

world.add_particles(
    Circle6Generator(
        700 + 300j,
        6,
        1,
        0
    )
)

prev_step = time.time()
frame_counter = 0
fps = 0

while 1:
    ct = time.time()
    if (ct - prev_step) > 1:
        fps = "{:.2f}".format(frame_counter / (ct - prev_step))
        prev_step = ct
        frame_counter = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    world.step()
    world.draw()
    world.write(fps)
    world.update()
    frame_counter += 1
