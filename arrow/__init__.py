import pygame
import math
import numpy as np


class Arrow:
    def __init__(self, start_pos, vector, tip_len_1, tip_len_2):
        self.vector = np.asarray(vector)
        self.pos = np.asarray(start_pos)
        self.tip_pos = np.array([start_pos[0] + vector[0], start_pos[1] + vector[1]])
        self.length = math.sqrt(vector[0]**2 + vector[1]**2)
        self.tip = self.get_triangle(tip_len_1, tip_len_2)

    def draw(self, screen, color, unit, origin):
        start = np.array([int(unit * self.pos[0]), int(-unit * self.pos[1])]) + np.asarray(origin)
        tip_pos = np.array([int(unit * self.tip_pos[0]), int(-unit * self.tip_pos[1])]) + np.asarray(origin)
        tip = []
        for point in range(len(self.tip)):
            tip.append(np.array([int(unit * self.tip[point][0]), int(-unit * self.tip[point][1])]) + np.asarray(origin))
        pygame.draw.line(screen, color, tuple(start), tuple(tip_pos), 2)
        pygame.draw.polygon(screen, color, tip)

    def get_triangle(self, tip_len_1, tip_len_2):
        l = tip_len_1
        d = tip_len_2
        h = math.sqrt(l ** 2 - (d / 2) ** 2)
        v_unit = self.vector / self.length
        v_unit_normal = np.array([-v_unit[1], v_unit[0]])
        b = self.tip_pos - h * v_unit
        c = b + d / 2 * v_unit_normal
        d = b - d / 2 * v_unit_normal
        return [self.tip_pos, c, d]
