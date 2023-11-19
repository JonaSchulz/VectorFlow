import copy
import random
from arrow import *
from param import *

# class for vector field including droplets
class Field:
    def __init__(self, param):
        self.ds = param.ds
        self.unit = param.unit
        self.size = param.size

        # droplet parameters:
        self.number_of_droplets = param.number_of_droplets
        self.droplet_color = param.droplet_color
        self.droplet_radius = param.droplet_radius
        self.renew_freq = param.renew_freq

        # path parameters:
        self.bool_path = (param.path_length > 0)
        self.path_length = param.path_length
        self.path_color = param.path_color
        self.path_width = param.path_width

        self.droplets = []
        self.origin = (param.size[0] // 2, param.size[1] // 2)  # location of the origin in the center of the screen

        # initialisation of droplets (calculating initial positions and appending to self.droplets list):
        # droplet_positions = Field.spread_points(self.number_of_droplets, param.size[0], param.size[1])
        # for i in range(len(droplet_positions)):
        #     self.droplets.append(Droplet((droplet_positions[i][0] - self.origin[0]) / self.unit,
        #                                  -(droplet_positions[i][1] - self.origin[1]) / self.unit, self.path_length))
        # initialisation of arrows (calculating positions and appending to self.arrows list):
        self.bool_arrows = param.bool_arrows
        self.bool_arrow_color = param.bool_arrow_color
        self.arrow_unit = arrow_unit
        if self.bool_arrows:
            arrow_positions = Field.spread_points(param.number_of_arrows, param.size[0], param.size[1])
            self.max_length_sq = 0
            self.arrows = self.get_arrows(param.arrow_length, arrow_positions)
            self.arrow_color = param.arrow_color
            self.arrow_length = param.arrow_length

    def generate_droplet(self):
        x_pos = random.randint(-self.size[0] // 2, self.size[0] // 2) / self.unit
        y_pos = random.randint(-self.size[1] // 2, self.size[1] // 2) / self.unit
        self.droplets.append(Droplet(x_pos, y_pos, self.path_length))

    def delete_droplet(self):
        index = random.randint(0, len(self.droplets) - 1)
        self.droplets[index].self_destruct()

    def renew_droplets(self, freq):
        for droplet in self.droplets:
            if abs(droplet.x) > self.size[0] / (2 * unit) * 1.5 or abs(droplet.y) > self.size[1] / (2 * unit) * 1.5:
                self.droplets.remove(droplet)
                self.generate_droplet()
        if len(self.droplets) != self.number_of_droplets:
            for i in range(self.number_of_droplets - len(self.droplets)):
                self.generate_droplet()
            for i in range(len(self.droplets) - self.number_of_droplets):
                self.delete_droplet()
        # for i in range(freq):
        #     self.generate_droplet()
        #     self.delete_droplet()

    # update all droplets by one integration step:
    def update(self):
        for droplet in self.droplets:
            droplet.update(self.ds)
            if droplet.dead:
                self.droplets.remove(droplet)
        self.renew_droplets(self.renew_freq)

    # display all droplets at current position on screen:
    def display(self, screen):
        if self.bool_arrows:
            self.draw_vectors(screen)
        # display paths trailing every droplet (if path_length > 0):
        if self.bool_path:
            for droplet in self.droplets:
                droplet.draw_path(screen, self.path_color, self.path_width, self.unit, self.origin)

        for droplet in self.droplets:
            droplet.draw_droplet(screen, self.droplet_color, self.droplet_radius, self.unit, self.origin)

    # returns Arrow objects based on length, field equation and arrow_positions:
    def get_arrows(self, length, positions):
        arrows = []
        max_length_sq = 0
        for position in positions:
            pos = (position[0] - self.origin[0]) / self.unit, (position[1] - self.origin[1]) / self.unit
            vector = np.asarray(get_vel(pos[0], pos[1]))
            if vector[0] ** 2 + vector[1] ** 2 > max_length_sq:
                max_length_sq = vector[0] ** 2 + vector[1] ** 2
            if vector[0]**2 or vector[1]**2:
                vector *= (1/(math.sqrt(vector[0]**2 + vector[1]**2)) * length)
                arrows.append(Arrow(pos, vector, 0.1, 0.1))
        self.max_length_sq = max_length_sq
        return arrows

    # displays all arrows on screen:
    def draw_vectors(self, screen):
        for arrow in self.arrows:
            arrow.draw(screen, self.get_arrow_color(get_vel(*arrow.pos)), self.arrow_unit, self.origin)

    def get_arrow_color(self, vel):
        if self.bool_arrow_color:
            length_sq = vel[0] ** 2 + vel[1] ** 2
            r = min(length_sq / self.max_length_sq * 255 + 50, 255)
            if length_sq / self.max_length_sq < 1/2:
                g = length_sq / self.max_length_sq * 512
            else:
                g = 512 - length_sq / self.max_length_sq * 512
            b = 255 - length_sq / self.max_length_sq * 255
            return r, g, b
        else:
            return self.arrow_color

    # function to calculate positions of n points evenly spread across the screen (based on width, height of screen):
    @classmethod
    def spread_points(cls, n, width, height):
        if n == 0:
            return []
        n_x = int(math.sqrt(width/height * n + (width - height)**2 / (4 * height**2)) - (width - height) / (2 * height))
        n_y = n // n_x
        dx = width // n_x
        dy = height // n_y
        positions = []
        for x in range(n_x):
            for y in range(n_y):
                positions.append([x * dx + dx//2, y * dy + dy//2])
        return positions


# class for a droplet:
class Droplet:
    def __init__(self, x, y, path_length=0):
        self.x = x
        self.y = y
        self.path_length = path_length  # defines number of steps in the past stored for path display
        self.past_pos = []  # stores past positions for path display
        self.clock = 0
        self.birth = True
        self.destruction_timer = 0
        self.destroy = False
        self.dead = False

    # update droplet position based on field equations and updates past_pos:
    def update(self, ds):
        try:
            v_x, v_y = get_vel(self.x, self.y)
        except OverflowError:
            del self
            return
        self.x += v_x * ds
        self.y += v_y * ds
        self.past_pos.append((self.x, self.y))
        if len(self.past_pos) >= self.path_length:
            self.past_pos.pop(0)
        self.clock += 1
        if self.destroy:
            self.destruction_timer += 1

    def self_destruct(self):
        if not self.birth:
            self.destroy = True

    # display droplet at current position on screen:
    def draw_droplet(self, screen, color_final, radius, unit, origin):
        color = self.get_brightness(color_final)
        if self.destroy and color == black:
            self.dead = True
        if self.birth and color == color_final:
            self.birth = False
        try:
            pygame.draw.circle(screen, color, (int(self.x * unit + origin[0]),
                                               int(-self.y * unit + origin[1])), radius)
        except OverflowError:
            del self
        except TypeError:
            del self

    # display path trailing the droplet:
    def draw_path(self, screen, color, width, unit, origin):
        for i in range(len(self.past_pos)):
            fade = 1 / len(self.past_pos)
            faded_color = tuple([i * fade * color[j] for j in range(len(color))])
            try:
                rect = pygame.rect.Rect(int(self.past_pos[i][0] * unit + origin[0]),
                                        int(-self.past_pos[i][1] * unit + origin[1]), width, width)
            except TypeError:
                pass
            pygame.draw.rect(screen, faded_color, rect)

    def get_brightness(self, color):
        fade = 0.01
        if self.destroy:
            return max(0, color[0] - int(fade * self.destruction_timer * color[0])), \
                   max(0, color[1] - int(fade * self.destruction_timer * color[1])), \
                   max(0, color[2] - int(fade * self.destruction_timer * color[2]))
        return min(color[0], int(fade * self.clock * color[0])), min(color[1], int(fade * self.clock * color[1])), \
            min(color[2], int(fade * self.clock * color[2]))


# class for storage and display of simulation render:
class Render:
    def __init__(self, field):
        self.field = field  # Field object to render
        self.render_list = []   # stores field information over entire render time period

    # render field simulation over n integration steps:
    def render(self, n):
        for time in range(n):
            self.render_list.append([])
            for droplet in self.field.droplets:
                drop = copy.copy(droplet)   # droplet object can't be stored directly since it should not be updated
                drop.past_pos = list(droplet.past_pos)  # I have no idea why this is necessary but it is
                self.render_list[time].append(drop)     # add Droplet object at current time to render_list
            self.field.update()

    # play the rendered simulation:
    def play_render(self, screen, wait_time, bool_arrows=False):
        for time in range(len(self.render_list)):
            screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # display paths if path_length > 0:
            if self.field.bool_path:
                for droplet in self.render_list[time]:
                    droplet.draw_path(screen, self.field.path_color, self.field.path_width, self.field.unit,
                                      self.field.origin)
            # display droplets:
            for droplet in self.render_list[time]:
                droplet.draw_droplet(screen, self.field.droplet_color, self.field.droplet_radius, self.field.unit,
                                     self.field.origin)
            # display arrows if arrow_length > 0:
            if bool_arrows:
                self.field.draw_vectors(screen)

            pygame.display.flip()
            pygame.time.wait(wait_time)

