import sys, pygame
from itertools import product

from particle import Particle
from simmetric_dict import Dict
from time import time
from random import random

pygame.init()

size = width, height = 1800, 1000
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

WHITE = (255, 255, 255)

particles = [Particle(screen, x*1j + y, speed=30) for x, y in product(range(200, 235, 5), range(200, 235, 5))]

particles += [Particle(screen, x*1j + y + 1, speed=-30) for x, y in product(range(200, 235, 5), range(350, 385, 5))]


particles += [Particle(screen, 0.5, speed=10j+10)]

particles += [
    Particle(screen, 71j + 70, speed=1j),
    Particle(screen, 71j + 80, speed=-1j)

]

F = Dict(particles)
dT = 0.05

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
                if id(a) < id(b):
                    F[(a, b)] = a.F(b)

    for p in particles:
        EF = sum(F.values_by(p))
        p.add(EF, dT)
        p.move(dT)

    screen.fill(black)
    for p in particles:
        p.draw()
    pygame.display.flip()
    frame_counter += 1
    t2 = time()