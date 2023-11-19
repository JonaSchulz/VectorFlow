from math import *
from .functions import *
import numpy as np

size = 1800, 950
black = 0, 0, 0
white = 255, 255, 255
blue = 45, 74, 83
cyan = 20, 150, 150
red = 180, 40, 40
green = 30, 190, 60

wait_time = 0
number_of_droplets = 1000
unit = 100
arrow_unit = 100
ds = 0.005

display_arrows = False
show_color = True
number_of_arrows = 500
arrow_length = 0.3
arrow_color = white

droplet_color = cyan
droplet_radius = 4
renew_freq = 10

path_color = blue
path_length = 0
path_width = 2

grid_color = white
steps = 500


def get_vel(x, y):
    # return moebius(x, y, 1, 1, -1, 1)
    # return exponential(x, y, b=1)
    # return charged_conducting_sphere(x, y, 1, np.zeros(2), -1/3) + point_charge(x, y, np.array([3, 0]), 1)
    # return point_charge(x, y, np.array([1/3, 0]), -1/3) + point_charge(x, y, np.array([3, 0]), 1) \
     #     + point_charge(x, y, np.zeros(2), 2 + 1/3)

    # return mathematical_dipole(x, y, np.zeros(2), np.array([0.1, 0]))
    # return charged_sphere(x, y, 0.01, (0, 0.01), -1) + charged_sphere(x, y, 0.01, (0, -0.01), 1)

    # return exp(x) * cos(y), exp(x) * sin(y)
    # return -x - y, x
    # return 2*x + x**2 - y**2, 2*y + 2*x*y
    # return sin(2 * y) + x / 5, cos(2 * x) + y / 5
    # return 1 / ((x-2) ** 2 + y ** 2) * (x-2) - 4 / ((x+2) ** 2 + y ** 2) * (x+2) , \
    #       1 / ((x-2) ** 2 + y ** 2) * y - 4 / ((x+2) ** 2 + y ** 2) * y
    # return np.log(x ** 2 + y ** 2), np.arctan2(y, x) + 2 * np.pi * 0    # complex logarithm
    # return x / np.sqrt(x ** 2 + y ** 2), y / np.sqrt(x ** 2 + y ** 2)
    # return 2 * x, -2 * y
    return cosh(y), sinh(x)
    # return acos(sin(y)), acos(sin(x))
    # return acos(sin(y)), asin(cos(x))
    # return exp(y) - exp(x), exp(x) - exp(y)
    # return exp(-abs(y)), exp(-abs(x))

    # return x ** 2 + y ** 2, np.arctan2(y, x)
    # return x * cos(y), x * sin(y)     # transform polar to cartesian coordinates
    # return x * cos(y), y * cos(x)
    # return np.sqrt(x ** 2 + y ** 2), np.arctan2(y, x)
    # return exp(-y) * sin(y), exp(-x) * cos(x)

    # return sin(y), sin(x)
    # return cos(y), sin(x)
    # return cos(x) * sin(y), -sin(x) * cos(y)

    # return 0, -abs(y) - 10
    # return x, y
    # return y**2 + x**2, (abs(y)+1)**x
    # return y**2, 0
    # return 2 * x + y, x + 2 * y       # linear transformation
    # return -y / 2, x / 2      # 90° rotation
    # return x ** 2 - y ** 2, -2 * x * y

# class for Field initialisation parameters (Field() takes FieldParam object as parameter):
class FieldParam:
    def __init__(self, number_of_droplets=number_of_droplets, ds=ds, unit=unit, arrow_unit=arrow_unit, droplet_color=droplet_color,
                 droplet_radius=droplet_radius, renew_freq=renew_freq, path_color=path_color, path_width=path_width,
                 path_length=path_length, bool_arrows=display_arrows, bool_arrow_color=show_color,
                 number_of_arrows=number_of_arrows, arrow_length=arrow_length, arrow_color=arrow_color, size=size):
        self.number_of_droplets = number_of_droplets
        self.ds = ds    # integration step
        self.unit = unit    # number of pixels that represent distance 1 in vector field
        self.arrow_unit = arrow_unit
        self.droplet_color = droplet_color
        self.droplet_radius = droplet_radius
        self.renew_freq = renew_freq
        self.path_color = path_color
        self.path_width = path_width
        self.path_length = path_length
        self.bool_arrows = bool_arrows
        self.bool_arrow_color = bool_arrow_color
        self.number_of_arrows = number_of_arrows
        self.arrow_length = arrow_length
        self.arrow_color = arrow_color
        self.size = size    # size of screen
        self.grid_color = grid_color
        self.steps = steps