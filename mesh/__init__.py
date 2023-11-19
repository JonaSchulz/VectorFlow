import numpy as np
import pygame
from param import *


class Vertex:
    def __init__(self, pos, neighbours):
        self.x = pos[0]
        self.y = pos[1]
        self.neighbours = neighbours

    def get_pos(self):
        return np.array([self.x, self.y])


class Mesh:
    def __init__(self, vertices=[], adj_list=[]):
        self.vertices = vertices
        self.adj_list = adj_list

    def add_vertex(self, pos, neighbours=[]):
        for neighbour in neighbours:
            if neighbour > len(self.vertices):
                neighbours.remove(neighbour)
        self.vertices.append(Vertex(pos, neighbours))
        self.adj_list.append(neighbours)
        for neighbour in neighbours:
            self.adj_list[neighbour].append(len(self.vertices) - 1)

    def del_vertex(self, vertex):
        if type(vertex) is int:
            try:
                self.vertices.pop(vertex)
                for neighbour in self.adj_list[vertex]:
                    self.adj_list[neighbour].remove(vertex)
                self.adj_list.pop(vertex)
                return 0
            except IndexError:
                return 1
        elif isinstance(vertex, Vertex):
            for neighbour in vertex.neighbours:
                self.adj_list[neighbour].remove(self.vertices.index(vertex))
            self.adj_list.pop(self.vertices.index(vertex))
            self.vertices.remove(vertex)
            return 0
        return 1

    def draw(self, screen, color, unit, screen_origin, width=2):
        lines = []
        for vertex in self.vertices:
            index = self.vertices.index(vertex)
            for neighbour in vertex.neighbours:
                if (vertex, self.vertices[neighbour]) in lines or (vertex, self.vertices[neighbour]) in lines:
                    pass
                else:
                    lines.append((vertex, self.vertices[neighbour]))
        for line in lines:
            start_pos = (line[0].x * unit + screen_origin[0], -line[0].y * unit + screen_origin[1])
            end_pos = (line[1].x * unit + screen_origin[0], -line[1].y * unit + screen_origin[1])
            pygame.draw.line(screen, color, start_pos, end_pos, width)

    @staticmethod
    def get_grid(grid_spacing, size, unit, origin_spec="center"):
        mesh = Mesh([], [])
        n_x = int(size[0] / (unit * grid_spacing) + 1)
        n_y = int(size[1] / (unit * grid_spacing) + 1)
        for i in range(n_x):
            for j in range(n_y):
                if i == 0 and j == 0:
                    neighbours = []
                elif i == 0:
                    neighbours = [j - 1]
                elif j == 0:
                    neighbours = [(i - 1) * n_y]
                else:
                    neighbours = [i * n_y + j - 1, (i - 1) * n_y + j]
                if origin_spec == "center":
                    origin = np.array([size[0] // (2 * unit), -size[1] // (2 * unit)])
                elif origin_spec == "top-center":
                    origin = np.array([size[0] // (2 * unit), 0])
                elif origin_spec == "bottom-center":
                    origin = np.array([size[0] // (2 * unit), -size[1] // unit])
                elif origin_spec == "left-center":
                    origin = np.array([0, -size[1] // (2 * unit)])
                elif origin_spec == "right-center":
                    origin = np.array([size[0] // unit, -size[1] // (2 * unit)])
                pos = grid_spacing * np.array([i, -j]) - origin
                mesh.add_vertex(pos, neighbours)
        return mesh


class Transformation:
    def __init__(self, grid_spacing, size, unit, steps, origin="center"):
        self.unit = unit
        self.steps = steps
        self.steps_left = steps
        self.mesh = Mesh.get_grid(grid_spacing, size, unit, origin)
        self.transform_positions = self.get_transform_positions()
        self.transform_vectors = self.get_transform_vectors()

    def get_transform_positions(self):
        pos = []
        for vertex in self.mesh.vertices:
            pos.append(np.asarray(get_vel(vertex.x, vertex.y)))
        return pos

    def get_transform_vectors(self):
        vectors = []
        for i in range(len(self.mesh.vertices)):
            vectors.append(self.transform_positions[i] - self.mesh.vertices[i].get_pos())
        return vectors

    def transform(self):
        if self.steps_left:
            for i in range(len(self.mesh.vertices)):
                self.mesh.vertices[i].x += self.transform_vectors[i][0] / self.steps
                self.mesh.vertices[i].y += self.transform_vectors[i][1] / self.steps
            self.steps_left -= 1

    def inverse_transform(self):
        if self.steps - self.steps_left:
            for i in range(len(self.mesh.vertices)):
                self.mesh.vertices[i].x -= self.transform_vectors[i][0] / self.steps
                self.mesh.vertices[i].y -= self.transform_vectors[i][1] / self.steps
            self.steps_left += 1

    def draw(self, screen, color, screen_origin):
        self.mesh.draw(screen, color, self.unit, screen_origin)





