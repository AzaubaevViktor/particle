import sys
import time
import pygame

from world import World, SingleGenerator, RectGenerator, Circle4Generator, \
    Circle6Generator, Rect6Generator, t2c

world = World(
    friction=0.,
    dT=0.01,
    zoom=2,
)

# world.add_particles(
#     SingleGenerator(500+100j, 1)
# )
#
# world.add_particles(
#     SingleGenerator(500 + 200j, -2)
# )


world.add_particles(
    Circle6Generator(
        -200 + 200j,
        6,
        1,
        30
    )
)

world.add_particles(
    Circle6Generator(
        200 + 200j,
        6.5,
        1,
        -30
    )
)

prev_step = time.time()
frame_counter = 0
fps = "0"
movement = False

while 1:
    ct = time.time()
    if (ct - prev_step) > 1:
        fps = "{:.2f}".format(frame_counter / (ct - prev_step))
        prev_step = ct
        frame_counter = 0

    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            sys.exit()
        # Zoom
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                world.change_zoom(world.zoom / 10, t2c(event.pos))
            elif event.button == 5:
                world.change_zoom(-world.zoom / 10, t2c(event.pos))

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and not movement:
                print(world.m2w(t2c(event.pos)))
                world.add_particles(
                    SingleGenerator(
                        world.m2w(t2c(event.pos))
                    )
                )

        if event.type == pygame.KEYDOWN:
            if event.unicode == '+':
                world.dT += world.dT / 10
            elif event.unicode == '-':
                world.dT -= world.dT / 10

        movement = False
        if event.type == pygame.MOUSEMOTION:
            if event.buttons == (1, 0, 0):
                world.pov += t2c(event.rel)
                movement = True

    world.step()
    world.draw_grid()
    world.draw()
    world.write(fps + ", dT: {}".format(world.dT))
    world.update()
    frame_counter += 1
