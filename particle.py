import cmath

import pygame

coulumb_k = 256
repulshion_k = 3*16

WHITE = (255, 255, 255)


def normalize(z):
    return z / abs(z)


def __F(r: float, charge: int):
    coulumb = coulumb_k * charge / abs(r) ** 2
    repulshion = repulshion_k / abs(r)

    return coulumb - repulshion


def precalc():

    dr = 0.1
    to = 200
    data = {}

    for r in range(1, int(to / dr)):
        data[r] = __F(r * dr, 1)

    def _F(r: complex, charge: int):
        ra = abs(r)
        ra = 0.1 if 0 == ra else ra

        key_left = int(ra / dr)
        key_right = key_left + 1

        dlk = ra - key_left * dr
        drk = key_right * dr - ra

        if key_right not in data or key_left == 0:
            v = __F(ra, 1)
        else:
            v = data[key_left] * dlk + data[key_right] * drk

        return v * normalize(r)

    return _F


_F = precalc()


draw_k = 2

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
                           (int(self.pos.real * draw_k), int(self.pos.imag * draw_k)),
                           2)

    def __lt__(self, other: "Particle"):
        return self.id < other.id

