import pygame, os

from .graphics import Color, Image

class Interface(object):
    """@brief Pygame interface for controller to use.

    Use defaults to simplify screen/display creation.
    Icon path is specified from top level of pyngine.
    """

    def __init__(self, window_text='Pyngine', resolution=(400,400), grid_width=40, grid_height=40, refresh_rate=60, icon_path='icon.png'):
        """@brief Initialize the Pygame Interface object. \\
        @param window_text The text which appears on top of the window. \\
        @param resolution The tuple which determines the (height, width) in pixels of the window. \\
        @param grid_width Number of grids wide to use as a grid template. \\
        @param grid_height Number of grids high to use as a grid template. \\
        @param refresh_rate The target frame rate to run the window at. \\
        @param icon_path The path to the window's icon relative to the top level of Pyngine.
        """

        # pygame initialization
        pygame.init()
        pygame.font.init()

        # screen definitions
        self.resolution = resolution
        self.aspect_ratio = resolution[0] / resolution[1]
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.tile_width = resolution[0] / self.grid_width
        self.tile_height = resolution[1] / self.grid_height
        self.center = (self.resolution[0] / 2, self.resolution[1] / 2)
        self.area = [0, 0, self.resolution[0], self.resolution[1]]

        # how long each frame SHOULD take
        self.refresh_rate = refresh_rate
        self.frame_time = 1 / self.refresh_rate

        # top level of pyngine
        self.package_dir = os.path.dirname(os.path.join(os.path.abspath(__file__)))
        self.package_dir = os.path.abspath(os.path.join(self.package_dir, '..'))
        abs_icon_path = os.path.abspath(os.path.join(self.package_dir, icon_path))

        # pygame variables and initialization
        self.display = pygame.display.set_mode(self.resolution)
        icon = Image(abs_icon_path)
        pygame.display.set_icon(icon.surf)
        pygame.display.set_caption(window_text)
        pygame.display.update()
        self.clock = pygame.time.Clock()

        # calling close is the same as calling pygame.quit()
        self.close = pygame.quit

    def get_mouse_tile(self):
        """@return The x, y tile that the mouse is in.
        """
        x, y = pygame.mouse.get_pos()
        tx = x // self.tile_width
        ty = y // self.tile_height
        return (tx, ty)

    def get_tile_pixel(self, tx, ty):
        """@return The top left x, y pixel that tile tx, ty is at.
        """
        return (tx * self.tile_width, ty * self.tile_height)

    def update(self):
        """@brief Update Pygame based on clock and refresh rate.
        """
        pygame.display.update()
        self.clock.tick(self.refresh_rate)

    def clear(self):
        """@brief Set the screen to black
        """
        pygame.draw.rect(self.display, Color['black'], self.area)

