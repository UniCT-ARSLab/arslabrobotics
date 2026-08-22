#
# geometry.py
#

__all__ = [
    "normalize_angle",
    "rototranslate",
    "global_to_local",
    "local_to_global"
    ]

import math

def normalize_angle(a : float) -> float:
    """
    Normalizes an angle between -Pi and Pi
    """
    while a > math.pi:
        a = a - 2 * math.pi
    while a < - math.pi:
        a = a + 2 * math.pi
    return a


def rototranslate(xp, yp, xc, yc, t):
    """
    Rototranslate a point from a reference system (x',y') to a system (x,y)

    :param xp: The x' of the point in the reference system (x', y')
    :param yp: The y' point in the reference system (x', y')
    :param xc: The origin x of (x',y') in (x,y) coordinates
    :param yc: The origin y of (x',y') in (x,y) coordinates
    :param t: The rotation of x' with respect to x (in radians)

    """
    cos_t = math.cos(t)
    sin_t = math.sin(t)
    global_point_x = xc + xp * cos_t - yp * sin_t
    global_point_y = yc + xp * sin_t + yp * cos_t
    return global_point_x, global_point_y


def global_to_local(xc : float, yc : float, t : float, x : float, y : float) -> tuple:
    """
    Converts the coordinates from a global 2D reference system to a local one

    :param xc: The origin x of the local system in global coordinates
    :param yc: The origin y of the local system in global coordinates
    :param t: The rotation of the local system with respect to the global one (in radians)
    :param x: The point x in global coordinates
    :param y: The point y in global coordinates
    :return: The point (x, y) in local coordinates

    """
    cos_t = math.cos(t)
    sin_t = math.sin(t)
    dx = x - xc
    dy = y - yc
    local_x = dx * cos_t + dy * sin_t
    local_y = - dx * sin_t + dy * cos_t
    return local_x, local_y


def local_to_global(xc : float, yc : float, t : float, x : float, y : float) -> tuple:
    """
    Converts the coordinates from a local 2D reference system to a global one

    :param xc: The origin x of the local system in global coordinates
    :param yc: The origin y of the local system in global coordinates
    :param t: The rotation of the local system with respect to the global one (in radians)
    :param x: The point x in local coordinates
    :param x: The point y in local coordinates
    :return: The point (x, y) in global coordinates

    """
    cos_t = math.cos(t)
    sin_t = math.sin(t)
    global_point_x = xc + x * cos_t - y * sin_t
    global_point_y = yc + x * sin_t + y * cos_t
    return global_point_x, global_point_y
