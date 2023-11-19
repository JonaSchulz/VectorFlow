import pygame

from param import FieldParam
from arrow import *
from field import *
from mesh import *

param = FieldParam()
field = Field(param)
render = Render(field)

# coordinate_grid_2 = Mesh.get_grid(0.5, size, param.unit)
#coordinate_grid = Mesh.get_grid(1, size, param.unit)

grid = Transformation(0.4, (500, 500), param.unit, param.steps, origin="center")

# render.render(1000)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
stop = False
reverse = False

while True:
    # render.play_render(screen, wait_time, display_arrows)
    clock.tick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                stop = not stop
            elif event.key == pygame.K_SPACE:
                grid = Transformation(0.4, (500, 500), param.unit, param.steps, origin="center")
                screen.fill(black)
                grid.draw(screen, param.grid_color, (size[0] // 2, size[1] // 2))
            elif event.key == pygame.K_r:
                reverse = not reverse

    if not stop:
        screen.fill(black)
        #field.display(screen)
        #field.update()

        #coordinate_grid.draw(screen,  (40, 40, 40), param.unit, (size[0] // 2, size[1] // 2))
        grid.draw(screen, param.grid_color, (size[0] // 2, size[1] // 2))
        if reverse:
            grid.inverse_transform()
        else:
            grid.transform()

        pygame.time.wait(wait_time - clock.get_time())
    pygame.display.flip()
