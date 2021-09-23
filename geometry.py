"""Functions to define basic CAD building blocks."""
from os.path import abspath, dirname, join

from madcad import Axis, Circle, Segment, extrusion, flatsurface, thicken, vec3, web


def build_plate(x, y, z):
    """Build plate.

    Parameters
    ----------
    x : float
        Dimension in x direction.
    y : float
        Dimension in y direction.
    z :  float
        Dimension in z direction.

    Returns
    -------
    mesh
        A plate object.

    """
    A = vec3(0, 0, 0)
    B = vec3(x, 0, 0)
    line = web([Segment(A, B)])
    face = extrusion(vec3(0, y, 0), line)
    plate = thicken(face, z)
    return plate


def build_cylinder(x, y, h, r):
    """Build cylinder.

    Parameters
    ----------
    x : float
        Position in x.
    y : float
        Position in y.
    h : float
        Cylinder height.
    r : float
        Cylinder radius.

    Returns
    -------
    mesh
        A cylinder object.

    """
    A = vec3(x, y, h)
    B = vec3(0.0, 0.0, 1.0)
    axis = Axis(A, B)
    circle = flatsurface(Circle(axis, r))
    cylinder = thicken(circle, 3 * h)
    return cylinder
