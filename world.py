import math

import pygame

from particle import Particles, force_func, Particle, force_func
from particle_numpy import ParticlesNumpy


def c2t(c: complex) -> tuple:
    return c.real, c.imag


def t2c(t: tuple) -> complex:
    return t[0] + t[1] * 1j


def setin_factory(_min:float, _max:float):
    def f(value: float) -> float:
        return max(min(_max, value), _min)
    return f


class World:
    max_grid_lines = 15

    def __init__(
            self,
            width=1800,
            height=1000,
            dT=0.05,
            zoom=1,
            friction=0.01
    ):
        self.width = width
        self.height = height
        self.dT = dT
        self._zoom = zoom  # px by 1
        self.friction = friction

        self.pov = self.width / 2 + self.height / 2 *1j

        pygame.init()

        pygame.display.set_caption('Particle Simulator')
        self.fps_font = pygame.font.SysFont('Arial', 25)
        self.grid_font = pygame.font.SysFont('Verdana', min(min(self.height, self.width) // 80, 12))

        self.screen = pygame.display.set_mode(self._size)
        self.particles = ParticlesNumpy()

    def change_zoom(self, d_zoom: float, monitor_pos: complex):
        if self._zoom + d_zoom > 0:
            self.pov = d_zoom * (self.pov-monitor_pos) / self._zoom + self.pov
            self._zoom += d_zoom

    @property
    def zoom(self):
        return self._zoom

    @property
    def _size(self):
        return self.width, self.height

    def step(self):
        # calc forces
        self.particles.calc_forces(force_func)
        # set forces
        self.particles.step(self.dT, self.friction)
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
        for particle in self.particles.particles():
            pos = self.pov + particle.pos * self.zoom
            x = int(round(pos.real))
            y = int(round(pos.imag))

            pygame.draw.circle(
                self.screen,
                self.particle_color(particle),
                (x, y),
                2
            )

    def m2w(self, monitor_coord: complex) -> complex:
        return (monitor_coord - self.pov) / self.zoom

    def w2m(self, world_coord: complex) -> complex:
        return world_coord * self.zoom + self.pov

    def draw_grid(self):
        center = t2c((self.width / 2, self.height / 2))

        setin_y = setin_factory(0, self.height - 20)
        setin_x = setin_factory(0, self.width - 20)

        width_in = self.width / self.zoom
        height_in = self.height / self.zoom

        x_res = 10 ** -math.floor(
            -math.log(width_in / self.max_grid_lines, self.max_grid_lines))
        y_res = 10 ** -math.floor(
            -math.log(height_in / self.max_grid_lines, self.max_grid_lines))

        res = min(x_res, y_res)

        d_i = self.pov / self.zoom / res

        # X

        x_count = int(width_in / res)
        dx_i = int(d_i.real)

        for x_i in range(-dx_i - 1,  x_count - dx_i + 1):
            x = x_i * self.zoom * res + self.pov.real

            color = (200, 200, 200) if x_i == 0 else (50, 50, 50)

            pygame.draw.line(self.screen,
                             color,
                             (x, 0),
                             (x, self.height), )
            self._grid_write(x_i * res, (x + 2, setin_y(self.pov.imag + 2)))

        # Y

        y_count = int(height_in // res)
        dy_i = int(d_i.imag)

        for y_i in range(-dy_i - 1, y_count - dy_i + 1):
            y = y_i * self.zoom * res + self.pov.imag

            color = (200, 200, 200) if y_i == 0 else (50, 50, 50)

            pygame.draw.line(self.screen,
                             color,
                             (0, y),
                             (self.width, y), )
            self._grid_write(y_i * res, (setin_x(self.pov.real + 2), y + 2))

    def update(self):
        pygame.display.flip()
        self.screen.fill((0, 0, 0))

    def write(self, text, pos=(0, 0), color=(255, 255, 255)):
        self.screen.blit(self.fps_font.render(str(text), True, color),
                         pos)

    def _grid_write(self, text, pos, color=(255, 255, 255)):
        self.screen.blit(self.grid_font.render(str(text), True, color),
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
