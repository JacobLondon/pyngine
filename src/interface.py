import pygame, os

from .graphics import Color, Image

class Interface(object):
    """@brief Pygame interface for controller to use.

    Use defaults to simplify screen/display creation.
    Icon path is specified from top level of pyngine.
    """

    def __init__(self, name, resolution, grid, refresh_rate, icon_path):
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
        self.swidth = resolution[0]
        self.sheight = resolution[1]
        self.aspect_ratio = resolution[0] / resolution[1]
        self.gwidth = grid[0]
        self.gheight = grid[1]
        self.px = resolution[0] / self.gwidth
        self.py = resolution[1] / self.gheight
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
        pygame.display.set_caption(name)
        pygame.display.update()
        self.clock = pygame.time.Clock()

    def mouse_gpixel(self):
        """@return The x, y tile that the mouse is in.
        """
        x, y = pygame.mouse.get_pos()
        tx = x // self.px
        ty = y // self.py
        return (tx, ty)

    def grid_pixel(self, gx, gy):
        """@return The top left x, y pixel that tile tx, ty is at.
        """
        return (gx * self.px, gy * self.py)

    def update(self):
        """@brief Update Pygame based on clock and refresh rate.
        """
        pygame.display.update()
        self.clock.tick(self.refresh_rate)
