from os.path import join, abspath, dirname
from madcad import (
    vec3,
    Segment,
    Axis,
    difference,
    Circle,
    web,
    extrusion,
    show,
    write,
    thicken,
    flatsurface,
)

DIR = dirname(abspath(__file__))

h = 3.0

# build plate
A = vec3(0, 0, 0)
B = vec3(100, 0, 0)
line = web([Segment(A, B)])
face = extrusion(vec3(0, 100, 0), line)
plate = thicken(face, h)

# build cylinder
C = vec3(50.0, 50.0, h)
D = vec3(0.0, 0.0, 1.0)
axis = Axis(C, D)
circle = flatsurface(Circle(axis, 10.0))
cylinder = thicken(circle, 3 * h)

# Create part from difference
part = difference(plate, cylinder)

# Export part (needs numpy-stl)
write(part, join(DIR, "plate_with_holes_1.stl"))
