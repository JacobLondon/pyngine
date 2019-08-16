import pygame

from .color import colors as Color

class Painter(object):
    """@brief Helper class to use Pygame for drawing lines/shapes/areas.
    """
    
    def __init__(self, interface):
        self.display = interface.display
        self.tile_width = interface.tile_width
        self.tile_height = interface.tile_height

    def fill_tile(self, gx, gy, color=Color['white']):
        """@brief Fill tile with color."""
        area = [gx * self.tile_width, gy * self.tile_height, self.tile_width, self.tile_height]
        pygame.draw.rect(self.display, color, area)

    def fill_area(self, x, y, width, height, color=Color['white']):
        """@brief Fill area with color."""
        area = [x, y, width, height]
        pygame.draw.rect(self.display, color, area)

    def draw_line(self, x0, y0, x1, y1, color=Color['white']):
        """@brief Draw line from x0, y0 to x1, y1."""
        pygame.draw.line(self.display, color, (x0, y0), (x1, y1))

    def draw_circle(self, x, y, radius, color=Color['white']):
        """@brief Draw a circle given the top left corner of a surrounding square."""
        pygame.draw.circle(self.display, color, (x, y), radius)

    def draw_triangle(self, x0, y0, x1, y1, x2, y2, color=Color['white']):
        """@brief Draw triangle border lines."""
        self.draw_line(x0, y0, x1, y1, color)
        self.draw_line(x1, y1, x2, y2, color)
        self.draw_line(x2, y2, x0, y0, color)

    def fill_triangle(self, x0, y0, x1, y1, x2, y2, color=Color['white']):
        """@brief Fill the triangle with color."""
        pointlist = [(x0, y0), (x1, y1), (x2, y2)]
        pygame.draw.polygon(self.display, color, pointlist)
