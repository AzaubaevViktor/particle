import sys, pygame
from itertools import product

from particle import Particle
from simmetric_dict import SDict
from time import time

pygame.init()

size = width, height = 640, 480
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

WHITE = (255, 255, 255)

particles = [Particle(screen, x*1j + y) for x, y in product(range(50, 65, 5), range(50, 65, 5))]

# particles += [Particle(screen, 0.5, speed=500j+500)]


F = SDict()
dT = 0.001

p_sec = time()
t2 = time()
frame_counter = 0
while 1:
    if (t2 - p_sec) > 1:
        print(frame_counter / (t2 -p_sec))
        p_sec = time()
        frame_counter = 0

    t1 = time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    for a in particles:
        for b in particles:
            if a != b:
                if (a, b) not in F:
                    F[(a, b)] = a.F(b)

    for p in particles:
        EF = sum([v for v in F.values_by(p)])
        p.add(EF, dT)
        p.move(dT)

    screen.fill(black)
    for p in particles:
        p.draw()
    pygame.display.flip()
    frame_counter += 1
    t2 = time()