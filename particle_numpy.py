from collections import Callable

import numpy as np

import typing

from particle import Particles, Particle, \
    coulumb_k, repulshion_k


class ParticlesNumpy(Particles):
    def __init__(self):
        self.pos = np.array([], dtype=np.complex)
        self.F = np.array([], dtype=np.complex)
        self.speed = np.array([], dtype=np.complex)

    def add_single(self, particle: Particle):
        self.pos = np.hstack((
            self.pos,
            np.array(particle.pos, dtype=np.complex)
        ))

        self.speed = np.hstack((
            self.speed,
            np.array(particle.speed, dtype=np.complex)
        ))

        self.F = np.hstack((
            self.F,
            np.zeros((1, ), dtype=np.complex)
        ))

    def calc_forces(self, func: Callable):
        pos = self.pos
        posv = np.vstack([pos] * pos.size)
        posvt = posv.transpose()
        r = posv - posvt  # r[x][y] --> POSx - POSy

        nr = r / abs(r)

        F = - (coulumb_k * abs(r ** -2) - repulshion_k * abs(r ** -1)) * nr

        for i in range(pos.size):
            F[i][i] = 0

        self.F = np.sum(F, axis=1)

    def step(self, dT, speed_k):
        self.speed += self.F * dT
        self.speed *= speed_k

        self.pos += self.speed * dT

    def particles(self) -> typing.Iterator[Particle]:
        for pos, F, speed in zip(self.pos, self.F, self.speed):
            p = Particle(pos, speed=speed)
            p.F = F
            yield p

    def __iter__(self):
        for pos, F, speed in zip(self.pos, self.F, self.speed):
            yield pos.real, pos.imag, F, speed





