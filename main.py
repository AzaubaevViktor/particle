import sys
import time
import pygame

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
