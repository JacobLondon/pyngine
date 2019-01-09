import pygame, copy

from .constants import Anchor, Font, Color
from .layout import Grid

class Component(object):

    def __init__(self, controller):

        pygame.font.init()
        self.controller = controller
        self.loc = (0, 0)
        self.anchored_loc = (0, 0)
        self.width = 0
        self.height = 0
        self.visible = True
        self.focused = False
        self.hovering = False
        self.container = []

        self.text = ''
        self.font = Font.standard
        self.foreground = Color.foreground
        self.background = Color.background
        self.anchor = Anchor.northwest

    # set the relative location determined by the anchor used
    def set_anchor(self):

        if self.anchor == Anchor.northwest:
            self.anchored_loc = self.loc
        elif self.anchor == Anchor.northeast:
            self.anchored_loc = (self.loc[0] - self.width, self.loc[1])
        elif self.anchor == Anchor.southwest:
            self.anchored_loc = (self.loc[0], self.loc[1] - self.height)
        elif self.anchor == Anchor.southeast:
            self.anchored_loc = (self.loc[0] - self.width, self.loc[1] - self.height)
        elif self.anchor == Anchor.center:
            self.anchored_loc = (self.loc[0] - self.width / 2, self.loc[1] - self.height / 2)

    def load(self):
        pass

    def refresh(self):
        if not self.visible:
            return

        x, y = copy.copy((self.controller.mouse_x, self.controller.mouse_y))
        self.hovering = self.within(x, y)
        x, y = copy.copy((self.controller.clicked_x, self.controller.clicked_y))
        self.focused = self.within(x, y)

        self.refresh_actions()
        self.draw()

    def refresh_actions(self):
        pass

    def draw(self):
        pass

    # determine if the coordinates are within itself
    def within(self, x, y):
        left = self.anchored_loc[0]
        right = self.anchored_loc[0] + self.width
        top = self.anchored_loc[1]
        bottom = self.anchored_loc[1] + self.height

        return left <= x <= right and top <= y <= bottom
