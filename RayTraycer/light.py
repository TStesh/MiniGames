from Graphix.RayTraycer.vec3 import Vec3
from math import pow, inf
from Graphix.RayTraycer.sphere import Sphere, closest_intersection


class Light:

    def __init__(self, light_type: str, intensity: float, char_vec: Vec3 = Vec3((0, 0, 0))):
        self.light_type = light_type
        self.intensity = intensity
        self.char_vec = char_vec


# функция отражения луча
def reflect_ray(r: Vec3, n: Vec3) -> Vec3:
    return n * ((n * r) * 2) - r


# compute_lighting
def compute_lighting(point: Vec3, normal: Vec3, v: Vec3, s, spheres: [Sphere], lights: [Light]) -> float:
    intens = 0

    for light in lights:
        if light.light_type == 'ambient':
            intens += light.intensity
        else:
            if light.light_type == 'point':
                l = light.char_vec - point
                t_max = 1
            else:
                l = light.char_vec
                t_max = inf

            # проверка тени
            shadow_sphere, shadow_t = closest_intersection(spheres, point, l, 0.001, t_max)
            if shadow_sphere is not None:
                continue

            # диффузность
            n_dot_l = normal * l.ort()
            if n_dot_l > 0:
                intens += light.intensity * n_dot_l

            # зеркальность
            if s != -1:
                r = reflect_ray(l, normal).ort()
                r_dot_v = r * v
                if r_dot_v > 0:
                    intens += light.intensity * pow(r_dot_v, s)

    return intens
