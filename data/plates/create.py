from os.path import join, abspath, dirname
from madcad import vec3, Segment, web, extrusion, show, write, thicken

DIR = dirname(abspath(__file__))

# build geometry
A = vec3(0, 0, 0)
B = vec3(100, 0, 0)
line = web([Segment(A, B)])
face = extrusion(vec3(0, 100, 0), line)
plate = thicken(face, 3.0)

# Export part (needs numpy-stl)
write(plate, join(DIR, "plate_1.stl"))
