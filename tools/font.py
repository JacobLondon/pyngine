import pygame

"""Hold a set of fonts and allow for user defined fonts"""
class Font(object):

    def __init__(self, font, interface):

        pygame.font.init()

        # details about the font created
        self.name = font
        # scale is the ratio of screen width / number of grids wide the screen is
        self.scale = interface.tile_width / 15

        # make a set of font point sizes for built in components to use
        self.set = {}
        # default fonts
        self.set['small'] = self.named_font(10)
        self.set['standard'] = self.named_font(20)
        self.set['large'] = self.named_font(40)

    """Add user defined fonts"""
    def __setitem__(self, key, val):
        self.set[key] = val

    """Get set fonts"""
    def __getitem__(self, key):
        return self.set[key]

    """Create a font from the specified name"""
    def named_font(self, point):
        return Font.create(self.name, point * self.scale)

    """Simplify creating a font"""
    @staticmethod
    def create(font_name, point):
        return pygame.font.SysFont(font_name, int(point))