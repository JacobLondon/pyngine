import pygame

from .constants import Color, Font

class Interface(object):

    def __init__(self, window_text, resolution, grid_width, grid_height, refresh_rate):

        # pygame tools
        pygame.init()
        pygame.font.init()
        self.resolution = resolution
        self.tile_width = resolution[0] / grid_width
        self.tile_height = resolution[1] / grid_height
        self.refresh_rate = refresh_rate
        self.frame_time = 1 / self.refresh_rate
        self.display = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption(window_text)
        pygame.display.update()
        self.clock = pygame.time.Clock()

    def close(self):
        pygame.quit()

    # call to update the screen
    def update(self):
        # update loaded images
        #pygame.display.flip()
        pygame.display.update()
        self.clock.tick(self.refresh_rate)

    # draw a tile defined in config
    def draw_tile(self, x, y, color):
        area = [x, y, self.tile_width, self.tile_height]
        pygame.draw.rect(self.display, color, area)

    # draw a sprite on a tile
    def draw_sprite(self, sprite):
        self.draw_tile(sprite.loc[0], sprite.loc[1], sprite.color)

    # draw a given area
    def draw_area(self, x, y, width, height, color):
        area = [x, y, width, height]
        pygame.draw.rect(self.display, color, area)

    def draw_line(self, x0, y0, x1, y1, color=Color.white):
        pygame.draw.line(self.display, color, (x0, y0), (x1, y1))

    def draw_triangle(self, x0, y0, x1, y1, x2, y2, color=Color.white):
        self.draw_line(x0, y0, x1, y1, color)
        self.draw_line(x1, y1, x2, y2, color)
        self.draw_line(x2, y2, x0, y0, color)

    # set the screen to background color
    def clear(self):
        area = [0, 0, self.resolution[0], self.resolution[1]]
        pygame.draw.rect(self.display, Color.background, area)
