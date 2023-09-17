from math import inf
from vec3 import Vec3

class Sphere:

    def __init__(self, center: Vec3, radius, color: Vec3, specular, reflective: float):
        self.center = center
        self.radius = radius
        self.color = color
        self.specular = specular
        self.reflective = reflective

    def intersect_ray(self, o: Vec3, d: Vec3) -> (float, float):
        oc = o - self.center
        k1, k2, k3 = d * d, oc * d, oc * oc - self.radius ** 2
        discr = k2 ** 2 - k1 * k3
        if discr < 0:
            return inf, inf
        t1 = (-k2 + discr ** .5) / k1
        t2 = (-k2 - discr ** .5) / k1
        return t1, t2


def closest_intersection(spheres: [Sphere], o: Vec3, d: Vec3, t_min: float, t_max: float) -> (Sphere, float):
    closest_t = inf
    closest_sphere = None
    for sphere in spheres:
        t1, t2 = sphere.intersect_ray(o, d)
        if t_min <= t1 <= t_max and t1 < closest_t:
            closest_t = t1
            closest_sphere = sphere
        if t_min <= t2 <= t_max and t2 < closest_t:
            closest_t = t2
            closest_sphere = sphere
    return closest_sphere, closest_t
