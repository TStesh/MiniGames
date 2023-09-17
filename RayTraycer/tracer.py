from math import inf
from vec3 import Vec3
from sphere import Sphere, closest_intersection
from light import Light, compute_lighting, reflect_ray
from threading import Thread


class Tracer:
    __aspect_ratio = 16 / 9

    def __init__(self, o: Vec3 = Vec3((0, 0, 0)), canvas_height=200, bg_color: Vec3 = Vec3((255, 255, 255))):
        self.canvas_height = canvas_height
        self.canvas_width = int(canvas_height * self.__aspect_ratio)
        self.viewport_size_y = 1
        self.viewport_size_x = self.viewport_size_y * self.__aspect_ratio
        self.viewport_dist = 1
        self.background_color = bg_color
        self.o = o

    def img_size(self) -> (int, int):
        return self.canvas_width, self.canvas_height

    # x, y - canvas coordinates
    def canvas_to_viewport(self, x, y) -> Vec3:
        return Vec3((
            x * self.viewport_size_x / self.canvas_width,
            y * self.viewport_size_y / self.canvas_height,
            self.viewport_dist
        ))

    # tracer: trace ray within scene
    def trace_ray(self, spheres: [Sphere], lights: [Light], o: Vec3, d: Vec3, t_min: float, t_max: float,
                  depth: int) -> Vec3:

        closest_sphere, closest_t = closest_intersection(spheres, o, d, t_min, t_max)

        if closest_sphere is None:
            return self.background_color

        # вычисление локального цвета
        point = o + d * closest_t
        normal = (point - closest_sphere.center)
        intens = compute_lighting(point, normal.ort(), -d.ort(), closest_sphere.specular, spheres, lights)
        local_color = closest_sphere.color * intens

        # Если мы достигли предела рекурсии или объект не отражающий, то мы закончили
        r = closest_sphere.reflective
        if depth <= 0 or r <= 0:
            return local_color

        # Вычисление отражённого цвета
        vec_r = reflect_ray(-d, normal)
        reflected_color = self.trace_ray(spheres, lights, point, vec_r, 0.001, inf, depth - 1)

        return local_color * (1 - r) + reflected_color * r

    # tracer main loop
    def main_loop(self, spheres: [Sphere], lights: [Light], rec_depth: int) -> [int]:
        start_x = self.canvas_width >> 1
        start_y = self.canvas_height >> 1
        pixels = []
        for y in range(-start_y, start_y):
            for x in range(-start_x, start_x):
                d = self.canvas_to_viewport(x, y)
                color = self.trace_ray(spheres, lights, self.o, d, 1, inf, rec_depth)
                for _ in range(3):
                    x = 255 if color.vec[_] > 255 else int(color.vec[_])
                    pixels.append(x)
        return pixels
