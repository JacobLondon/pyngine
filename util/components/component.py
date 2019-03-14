import pygame, copy

from ..graphics import Color
from ..mouse import Mouse
from .screen_object import ScreenObject

"""Parent component
Handles controller z index insertion, focus, and relative anchoring
"""
class Component(ScreenObject):

    def __init__(self, controller, parent=None, z=0):
        ScreenObject.__init__(self)
        pygame.font.init()

        # the controller the component belongs to can be auto refreshed
        self.controller = controller
        self.controller.add_component(self, z)

        # parent component's list of subcomponents
        if parent is not None:
            parent.subcomponents.append(self)

        # own subcomponent list
        self.subcomponents = []

        # tools for focus
        self.focused = False    # true for the frame after an 'unclick' on a component
        self.pressing = False   # true when mouse down on component
        self.pressed = False    # true when pressing first becomes true
        self.hovering = False   # true when mouse is over the component

        # anchor identifiers
        self.northwest = 0
        self.northeast = 1
        self.southeast = 2
        self.southwest = 3
        self.center = 4

        # default visual characteristics
        self.text = ''
        self.font = self.controller.font['standard']
        self.foreground = Color['white']
        self.background = Color['black']
        self.anchor = self.northwest
        self.anchored_loc = (0, 0)

    """Returns self.text at (x, y)"""
    def __str__(self):
        return "'" + str(self.text) + "' at " + str(self.anchored_loc)

    """Method meant to be overwritten by children to
    initialize visual attributes/subcomponents
    """
    def load(self):
        pass

    """Called every frame
    Handles giving children the same visibility, determining
    pressing/hovering/focus/drawing
    """
    def refresh(self):
        # ensure visibility is the same to children components
        for sub in self.subcomponents:
            sub.visible = self.visible

        # children, with parent will lose visibility
        if not self.visible:
            self.focused = False
            for sub in self.subcomponents:
                sub.focused = False

            # do make checks if not visible
            return

        # mouse within bounds of component
        x, y = copy.copy((self.controller.mouse.x, self.controller.mouse.y))
        self.hovering = self.within(x, y)

        # holding left click in the component
        x, y = copy.copy((self.controller.mouse.l_clicked_x, self.controller.mouse.l_clicked_y))
        self.pressing = self.within(x, y) and self.controller.mouse.presses[Mouse.l_click]

        self.determine_focus()

        # perform custom method overwritten by component children
        self.refresh_actions()
        self.draw()

    """Give/take focus from items clicked on"""
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

    """Do every frame if the component is visible.
    Meant to be overwritten by component children
    """
    def refresh_actions(self):
        pass

    """Do every frame if the component is visible.
    Meant to be overwritten by component children,
    called after refresh_actions.
    """
    def draw(self):
        pass

    """Set the relative location determined by the anchored specified"""
    def set_anchor(self):

        if self.anchor == self.northwest:
            self.anchored_loc = self.loc
        elif self.anchor == self.northeast:
            self.anchored_loc = (self.loc[0] - self.width, self.loc[1])
        elif self.anchor == self.southwest:
            self.anchored_loc = (self.loc[0], self.loc[1] - self.height)
        elif self.anchor == self.southeast:
            self.anchored_loc = (self.loc[0] - self.width, self.loc[1] - self.height)
        elif self.anchor == self.center:
            self.anchored_loc = (self.loc[0] - self.width / 2, self.loc[1] - self.height / 2)

    """Determine if the given coordinates are within the bounds of itself"""
    def within(self, x, y):
        left = self.anchored_loc[0]
        right = self.anchored_loc[0] + self.width
        top = self.anchored_loc[1]
        bottom = self.anchored_loc[1] + self.height

        return left <= x <= right and top <= y <= bottom
