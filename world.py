from typing import Tuple

import pygame
import math
from particle import Particles, force_func, Particle, force_func
from particle_numpy import ParticlesNumpy


class World:
    def __init__(
            self,
            width=1800,
            height=1000,
            dT=0.05,
            draw_k=1,
            friction=0.01
    ):
        self.width = width
        self.height = height
        self.dT = dT
        self.draw_k = draw_k
        self.speed_k = 1 - friction

        pygame.init()

        pygame.display.set_caption('Particle Simulator')
        self.font = pygame.font.SysFont('Arial', 25)

        self.screen = pygame.display.set_mode(self._size)
        self.particles = ParticlesNumpy()

    @property
    def _size(self):
        return self.width, self.height

    def step(self):
        # calc forces
        self.particles.calc_forces(force_func)
        # set forces
        self.particles.step(self.dT, self.speed_k)
        # wall
        # self.particles.wall(self.width, self.height)

    def particle_color(self, particle: Particle):
        speed_c = abs(particle.speed)
        force_c = abs(particle.F) * 5
        R = max(128, 255 - force_c)
        G = max(128, 255 - speed_c)
        B = 255 - force_c - speed_c
        return tuple(int(max(0, component)) for component in (R, G, B))

    def draw(self):
        self.screen.fill((0, 0, 0))

        for particle in self.particles.particles():
            pygame.draw.circle(
                self.screen,
                self.particle_color(particle),
                (int(round(particle.pos.real * self.draw_k)),
                 int(round(particle.pos.imag * self.draw_k))),
                2
            )

    def update(self):
        pygame.display.flip()

    def write(self, text, pos=(0, 0), color=(255, 255, 255)):
        self.screen.blit(self.font.render(str(text), True, color),
                         pos)

    def add_particles(self, generator):
        self.particles.add(generator)


class SingleGenerator:
    def __init__(self, pos: complex, speed: complex = 0):
        self.pos = pos
        self.speed = speed

    def __iter__(self):
        yield Particle(self.pos, speed=self.speed)


class RectGenerator:
    def __init__(self, start: complex, end:complex, density: float, speed: complex):
        self.start = start
        self.end = end
        self.density = density
        self.step = 1 / density
        self.speed = speed

    def __iter__(self):
        x = self.start.real
        while x < self.end.real:
            y = self.start.imag
            while y < self.end.imag:
                yield Particle(x + y*1j, speed=self.speed)
                y += self.step
            x += self.step


class Rect6Generator(RectGenerator):
    def __iter__(self):
        size = 1 / self.density

        r = self.end - self.start

        height = size * 2
        vert = height * 3 / 4
        width = 3 ** 0.5 / 2 * height
        horiz = width

        for x in range(int(r.real // size) + 1):
            for y in range(int(r.imag // size)):
                yield Particle(
                    self.start + (x * horiz + (- (x % 2) * size + y * height) * 1j),
                    speed=self.speed
                )

                print(x * height + y * width * 1j)


class Circle4Generator:
    generator_class = RectGenerator

    def __init__(self,
                 center: complex,
                 diameter: float,
                 density: float,
                 speed_linear: complex,
                 ):
        self.center = center
        self.diameter = diameter
        self.density = density
        self.speed_linear = speed_linear

    def __iter__(self):
        diag = self.diameter * (1 + 1j)
        r = self.generator_class(self.center - diag, self.center + diag, self.density, self.speed_linear)
        for particle in r:
            if abs(particle.pos - self.center) <= self.diameter:
                yield particle


class Circle6Generator(Circle4Generator):
    generator_class = Rect6Generator
