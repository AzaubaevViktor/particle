import sys, pygame
from itertools import product

from particle import Particle

pygame.init()

size = width, height = 640, 480
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

WHITE = (255, 255, 255)

particles = [Particle(screen, x*1j + y) for x, y in product(range(50, 105, 2), range(50, 105, 2))]

particles += [Particle(screen, 25.5, speed=500j+500)]


F = {}
dT = 0.001

for particle in particles:
    F[particle] = {}
    for particle2 in particles:
        if particle != particle2:
            F[particle][particle2] = 0


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    for a in particles:
        for b in particles:
            if a != b:
                F[a][b] = a.F(b)

    for p in particles:
        EF = sum([v for v in F[p].values()])
        p.add(EF, dT)
        p.move(dT)

    screen.fill(black)
    for p in particles:
        p.draw()
    pygame.display.flip()