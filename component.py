import pygame, copy

from .screen_object import ScreenObject
from .constants import Anchor, Font, Color, Mouse

class Component(ScreenObject):

    def __init__(self, controller, parent=None, in_foreground=True):
        ScreenObject.__init__(self)
        pygame.font.init()

        # the controller the component belongs to can be auto refreshed
        self.controller = controller
        if in_foreground:
            self.controller.foreground_components.append(self)
        else:
            self.controller.background_components.append(self)

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
        self.foreground = Color.foreground
        self.background = Color.background
        self.anchor = Anchor.northwest
        self.anchored_loc = (0, 0)

    def load(self):
        pass

    # always do before a refresh
    def prerefresh_actions(self):
        pass

    def refresh(self):
        self.prerefresh_actions()  

        # ensure visibility is the same to children components
        for sub in self.subcomponents:
            sub.visible = self.visible

        # children, like parent can lose visibility
        if not self.visible:
            self.focused = False
            for sub in self.subcomponents:
                sub.focused = False
            return

        # mouse within bounds of component
        x, y = copy.copy((self.controller.mouse_x, self.controller.mouse_y))
        self.hovering = self.within(x, y)

        # holding left click in the component
        x, y = copy.copy((self.controller.l_clicked_x, self.controller.l_clicked_y))
        self.pressing = self.within(x, y) and self.controller.mouse_presses[Mouse.l_click]

        self.determine_focus()
        self.refresh_actions()
        self.draw()

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

    def determine_focus(self):
        # component started being pressed on / positive edge of click
        if self.pressing and not self.pressed:
            self.pressed = True

        # the mouse leaves the bounds
        if not self.hovering:
            self.pressed = False

        # negative edge of click
        if self.pressed and not self.controller.mouse_presses[Mouse.l_click] and self.hovering:
            self.pressed = False
            self.focused = True

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
