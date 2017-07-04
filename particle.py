import cmath

import pygame

coulumb_k = 256
repulshion_k = 3*16

WHITE = (255, 255, 255)


def normalize(z):
    return z / abs(z)


def _F(r: complex, charge: int):
    coulumb = coulumb_k * charge / abs(r) ** 2
    repulshion = repulshion_k / abs(r)

    return (coulumb - repulshion) * normalize(r)


class Particle:
    _ID = 0

    def __new__(cls, *args, **kwargs):
        cls._ID += 1
        self = super(Particle, cls).__new__(cls)
        self.id = cls._ID
        return self

    def __init__(self, screen, pos: complex, charge: int = 1, speed: complex = 0):
        self.screen = screen
        self.pos = pos
        self.charge = charge
        self.speed = speed

    def F(self, p: "Particle"):
        d = (self.pos - p.pos)
        return _F(d, self.charge * p.charge)

    def add(self, F, dT):
        self.speed += F * dT

    def move(self, dT):
        self.pos += self.speed * dT

    def draw(self):
        pygame.draw.circle(self.screen, WHITE,
                           (int(self.pos.real * 4), int(self.pos.imag * 4)),
                           3)

    def __lt__(self, other: "Particle"):
        return self.id < other.id

