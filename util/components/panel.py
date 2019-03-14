import pygame

from .component import Component

"""A simple component used for displaying color"""
class Panel(Component):

    def __init__(self, controller, parent=None, z=0):
        Component.__init__(self, controller, parent, z)
        self.text = 'Panel'

    """Ensure the panel is anchored correctly"""
    def load(self):
        self.set_anchor()

    """Fill the area with color"""
    def draw(self):

        # draw the area of the panel
        self.controller.painter.fill_area(
            self.anchored_loc[0],
            self.anchored_loc[1],
            self.width,
            self.height,
            self.background)
