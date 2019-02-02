import pygame

from .constants import Color, Font

class Interface(object):

    def __init__(self, window_text='Pyngine', resolution=(400,400), grid_width=40, grid_height=40, refresh_rate=60):

        # pygame tools
        pygame.init()
        pygame.font.init()
        self.resolution = resolution
        self.tile_width = resolution[0] / grid_width
        self.tile_height = resolution[1] / grid_height
        self.center = (self.resolution[0] / 2, self.resolution[1] / 2)
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
        pygame.display.update()
        self.clock.tick(self.refresh_rate)

    # set the screen to background color
    def clear(self):
        area = [0, 0, self.resolution[0], self.resolution[1]]
        pygame.draw.rect(self.display, Color.background, area)
