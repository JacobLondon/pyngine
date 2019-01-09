import pygame, copy

from .constants import Color, Font, Anchor
from .component import Component
from .panel import Panel
from .label import Label
from .layout import Relative

class Textbox(Component):

    def __init__(self, controller, num_chars=15):
        Component.__init__(self, controller)
        self.num_chars = num_chars
        self.typing = False

        self.background = Color.white
        self.foreground = Color.black
        self.font = Font.large

        # textbox made with a label on a panel
        self.panel = Panel(self.controller)

        self.label = Label(self.controller, self.text)
        self.label.anchor = Anchor.northwest

    def load(self):

        self.width, self.height = self.font.size('o' * self.num_chars)
        self.set_anchor()

        self.panel.anchor = self.anchor
        self.panel.loc = self.loc
        self.panel.background = self.background
        self.panel.width = self.width
        self.panel.height = self.height
        self.panel.load()

        # update the label with button's members
        self.center_layout = Relative(self.panel)
        self.label.loc = self.center_layout.northwest
        self.label.text = self.text
        self.label.font = self.font
        self.label.foreground = self.foreground
        self.label.background = None
        self.label.load()

    def refresh_actions(self):
        # typing setup
        if self.focused and not self.typing:
            self.controller.typing = True
            self.typing = True
            self.controller.typed_text = copy.copy(self.text)
        # when the user is typing
        if self.focused and self.typing:
            self.text = copy.copy(self.controller.typed_text)
            self.controller.typed_text = self.controller.typed_text[:self.num_chars]
            self.load()

        # stop and start typing
        if not self.focused:
            self.typing = False
        if self.focused:
            self.typing = True

    def draw(self):
        self.panel.refresh()
        self.label.refresh()
