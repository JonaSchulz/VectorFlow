from math import *
import numpy as np

def charged_conducting_sphere(x, y, R, center, polarity, k=10000):
    if (x - center[0]) ** 2 + (y - center[1]) ** 2 >= R:
        scale = polarity * k * R / (sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2) ** 3)
        return scale * np.array([x - center[0], y - center[1]])
    else:
        return np.array([0, 0])


def mathematical_dipole(x, y, position, moment, k=100):
    r = np.array([x, y]) - position
    length_r = sqrt(r[0] ** 2 + r[1] ** 2)
    return k * (3 * np.dot(moment, r) * r / length_r ** 5) - moment / (length_r ** 3)


def dielectric_sphere(x, y, R, center, dielectric_1, dielectric_2=1, e_inf=1):
    if (x - center[0]) ** 2 + (y - center[1]) ** 2 >= R:
        return


def charged_sphere(x, y, R, center, charge_density, dielectric=1):
    k = charge_density / dielectric
    r = np.array([x, y]) - center
    length_r = sqrt(r[0] ** 2 + r[1] ** 2)
    if length_r > R:
        return k * R ** 3 / (3 * length_r ** 2) * np.array([x, y])
    else:
        return (-k * length_r ** 2 / 6 + k * R ** 2 / 2) * np.array([x, y])


def point_charge(x, y, position, charge, k=10000):
    dist = ((x - position[0]) ** 2 + (y - position[1]) ** 2)
    return k * charge * 1 / (dist ** 3) * (np.array([x, y]) - position)


def moebius(x, y, a, b, c, d):
    res = (a * (x + y * 1j) + b) / (c * (x + y * 1j) + d)
    if abs(res) < 10:
        return res.real, res.imag
    else:
        return 0, 0


def exponential(x, y, a=1, b=1):
    res = a * np.exp(b * (x + 1j * y))
    return res.real, res.imag