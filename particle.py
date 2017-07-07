import pygame

stable_point = 5
max_value = 2.25

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

    def _F(r: complex, charge: int):
        ra = abs(r)
        ra = dr if 0 == ra else ra

        key_left = int(ra / dr)
        key_right = key_left + 1

        if 0 < key_left < max_index - 1:
            dlk = ra - key_left * dr
            drk = key_right * dr - ra
            v = data[key_left] * dlk + data[key_right] * drk
        else:
            v = __F(ra, 1)

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
        self._F = F
        self.speed += F * dT

    def move(self, dT):
        self.pos += self.speed * dT

    @property
    def color(self):
        speed_d = abs(self.speed)
        force_d = abs(self._F) * 10
        R = 255 - force_d
        G = 255 - speed_d
        B = 255 - speed_d - force_d
        return tuple(int(max(0, component)) for component in (R, G, B))

    def draw(self):
        print(self.color)
        pygame.draw.circle(self.screen, self.color,
                           (int(self.pos.real * draw_k), int(self.pos.imag * draw_k)),
                           2)

    def __lt__(self, other: "Particle"):
        return self.id < other.id

