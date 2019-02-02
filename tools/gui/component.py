import pygame, copy

from ..graphics import Color
from ..constants import Anchor, Font
from ..mouse import Mouse
from .screen_object import ScreenObject

class Component(ScreenObject):

    def __init__(self, controller, parent=None, z=0):
        ScreenObject.__init__(self)
        pygame.font.init()

        # the controller the component belongs to can be auto refreshed
        self.controller = controller
        self.controller.add(self, z)

        # parent component's list of subcomponents
        if parent is not None:
            parent.subcomponents.append(self)

        self.focused = False
        self.pressing = False   # true when mouse down on component
        self.pressed = False    # true when pressing first becomes true
        self.hovering = False
        self.subcomponents = []

        self.text = ''
        self.font = Font.standard
        self.foreground = Color['white']
        self.background = Color['black']
        self.anchor = Anchor.northwest
        self.anchored_loc = (0, 0)

    def __str__(self):
        return "'" + str(self.text) + "' at " + str(self.anchored_loc)

    def load(self):
        pass

    def refresh(self):
        # ensure visibility is the same to children components
        for sub in self.subcomponents:
            sub.visible = self.visible

        # children, with parent will lose visibility
        if not self.visible:
            self.focused = False
            for sub in self.subcomponents:
                sub.focused = False
            return

        # mouse within bounds of component
        x, y = copy.copy((self.controller.mouse.x, self.controller.mouse.y))
        self.hovering = self.within(x, y)

        # holding left click in the component
        x, y = copy.copy((self.controller.mouse.l_clicked_x, self.controller.mouse.l_clicked_y))
        self.pressing = self.within(x, y) and self.controller.mouse.presses[Mouse.l_click]

        self.determine_focus()
        self.refresh_actions()
        self.draw()

    def determine_focus(self):
        # component started being pressed on / positive edge of click
        if self.pressing and not self.pressed:
            self.pressed = True
            self.focused = False

        # the mouse leaves the bounds
        if not self.hovering:
            self.pressed = False

        # negative edge of click
        if self.pressed and not self.controller.mouse.presses[Mouse.l_click] and self.hovering:
            self.pressed = False
            self.focused = True

    # do every frame for the component if it is visible
    def refresh_actions(self):
        pass

    def draw(self):
        pass

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

    # determine if the coordinates are within itself
    def within(self, x, y):
        left = self.anchored_loc[0]
        right = self.anchored_loc[0] + self.width
        top = self.anchored_loc[1]
        bottom = self.anchored_loc[1] + self.height

        return left <= x <= right and top <= y <= bottom
