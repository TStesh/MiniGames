from Graphix.RayTraycer.vec3 import Vec3
from Graphix.RayTraycer.sphere import Sphere
from light import Light
from Graphix.RayTraycer.tracer import Tracer
from Graphix.ppm import ppm6, ppm_view

fn = 'c:\\users\\alexa\\downloads\\scene.ppm'

spheres = [
    Sphere(Vec3((0, -1, 3)), 1, Vec3((255, 0, 0)), 500, 0.2),
    Sphere(Vec3((2, 0, 4)), 1, Vec3((0, 0, 255)), 500, 0.3),
    Sphere(Vec3((-2, 0, 4)), 1, Vec3((0, 255, 0)), 10, 0.4),
    Sphere(Vec3((0, -5001, 0)), 5000, Vec3((255, 255, 0)), 1000, 0.5)
]

lights = [
    Light('ambient', 0.2),
    Light('point', 0.6, Vec3((2, 1, 0))),
    Light('directional', 0.2, Vec3((1, 4, 4)))
]

tracer = Tracer(canvas_height=768, bg_color=Vec3((10, 20, 30)))

pixels = tracer.main_loop(spheres, lights, 3)

img_width, img_height = tracer.img_size()

ppm6(fn, img_width, img_height, pixels)

ppm_view(fn)
