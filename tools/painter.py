import pygame

from .constants import Color

class Painter(object):
    
    def __init__(self, controller):
        self.display = controller.interface.display
        self.tile_width = controller.interface.tile_width
        self.tile_height = controller.interface.tile_height

    # fill tile with color
    def fill_tile(self, gx, gy, color=Color.white):
        area = [gx * self.tile_width, gy * self.tile_height, self.tile_width, self.tile_height]
        pygame.draw.rect(self.display, color, area)

    # fill given area with color
    def fill_area(self, x, y, width, height, color=Color.white):

        area = [x, y, width, height]
        pygame.draw.rect(self.display, color, area)

    def draw_line(self, x0, y0, x1, y1, color=Color.white):
        pygame.draw.line(self.display, color, (x0, y0), (x1, y1))

    def draw_triangle(self, x0, y0, x1, y1, x2, y2, color=Color.white):

        self.draw_line(x0, y0, x1, y1, color)
        self.draw_line(x1, y1, x2, y2, color)
        self.draw_line(x2, y2, x0, y0, color)

    def fill_triangle(self, x0, y0, x1, y1, x2, y2, color=Color.white):
        pointlist = [(x0, y0), (x1, y1), (x2, y2)]
        pygame.draw.polygon(self.display, color, pointlist)
