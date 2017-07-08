from itertools import combinations
from typing import Callable, List

stable_point = 5
max_value = 1
max_force = 10

repulshion_k = 4 * stable_point * max_value
coulumb_k = repulshion_k * stable_point

print(repulshion_k, coulumb_k)

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
    data = [0 for _ in range(int(to / dr))]

    for r in range(1, int(to / dr)):
        data[r] = __F(r * dr, 1)

    max_index = len(data)

    def _F(p1: "Particle", p2: "Particle"):
        r = p1.pos - p2.pos
        ra = abs(r)
        ra = dr if 0 == ra else ra

        key_left = int(ra / dr)
        key_right = key_left + 1

        if 0 < key_left < max_index - 1:
            dlk = ra - key_left * dr
            drk = key_right * dr - ra
            v = data[key_left] * dlk + data[key_right] * drk
        elif 0 == key_left:
            return -max_force
        else:
            v = __F(ra, 1)

        return v * normalize(r)

    return _F


force_func = precalc()


draw_k = 2


class Particles:
    def __init__(self):
        self.list = []  # type: List[Particle]
        self._F = {}

    def calc_forces(self, func: Callable):
        """

        :param func: function(particle, particle) -> complex
        :return:
        """
        for p1, p2 in combinations(self.list, 2):
            F = func(p1, p2)
            self._F[p1][p2] = F
            self._F[p2][p1] = -F

    def step(self, dT, speed_k):
        for particle in self.list:
            particle.F = sum(self._F[particle].values())
            particle.apply_force(dT, speed_k=speed_k)
            particle.move(dT)

    def add(self, particles: List["Particle"]):
        for particle in particles:
            self.add_single(particle)

    def add_single(self, particle: "Particle"):
        for key in self._F:
            self._F[key][particle] = 0

        self._F[particle] = {}
        for p in self.list:
            self._F[particle][p] = 0

        self.list.append(particle)

    def wall(self, max_x, max_y):
        for particle in self.list:
            c = particle.pos
            x = c.real
            y = c.imag
            vx = particle.speed.real
            vy = particle.speed.imag

            if 0 > x:
                x = -x
                vx = -vx
            if 0 > y:
                y = -y
                vy = -vy
            if x > max_x:
                x = max_x - x
                vx = -vx
            if y > max_y:
                y = max_y - y
                vy = -vy

            particle.pos = x + y * 1j
            particle.speed = vx + vy * 1j

    def particles(self):
        return iter(self.list)

    def __iter__(self):
        for p in self.list:
            yield p.pos.real, p.pos.imag, p.F, p.speed


class Particle:
    _ID = 0

    def __new__(cls, *args, **kwargs):
        cls._ID += 1
        self = super(Particle, cls).__new__(cls)
        self.id = cls._ID
        return self

    def __init__(self, pos: complex, charge: int = 1, speed: complex = 0):
        self.pos = pos
        self.charge = charge
        self.speed = speed
        self._F = 0

    def F(self, p: "Particle"):
        d = (self.pos - p.pos)
        return force_func(d, self.charge * p.charge)

    @property
    def F(self):
        return self._F

    @F.setter
    def F(self, value):
        self._F = value

    def apply_force(self, dT, speed_k):
        self.speed += self._F * dT
        self.speed *= speed_k

    def move(self, dT):
        self.pos += self.speed * dT

    def __lt__(self, other: "Particle"):
        return self.id < other.id

