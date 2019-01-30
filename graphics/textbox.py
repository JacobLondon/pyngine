import pygame, copy, time
from threading import Thread

from .constants import Color, Font, Anchor
from .component import Component
from .panel import Panel
from .label import Label
from .layout import Relative

class Textbox(Component):

    def __init__(self, controller, num_chars=15, parent=None, z=0):
        Component.__init__(self, controller, parent, z)
        self.num_chars = num_chars
        self.typing = False
        self.cursor_active = False
        self.cursor_rate = 0.5

        self.background = Color.white
        self.foreground = Color.black
        self.font = Font.large

        # textbox made with a label on a panel
        self.panel = Panel(self.controller, parent=self)

        self.label = Label(self.controller, self.text, parent=self)

        self.width, self.height = self.font.size('o' * self.num_chars)

        self.cursor_label = Label(self.controller, '|')
        self.cursor_label.visible = False

    def load(self):

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

        # keep the cursor on the far right of the text
        w = self.label.font.size(self.label.text)[0]
        self.cursor_label.loc = self.center_layout.northwest
        self.cursor_label.loc = (self.cursor_label.loc[0] + w, self.cursor_label.loc[1])
        self.cursor_label.font = self.font
        self.cursor_label.foreground = self.foreground
        self.cursor_label.background = None
        self.cursor_label.load()

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

        # start/stop typing
        self.typing = self.focused

        # setup cursor flashing
        if self.typing and not self.cursor_active:
            self.cursor_active = True
            Thread(target=self.flash_cursor, daemon=True).start()

    def draw(self):
        self.panel.refresh()
        self.label.refresh()
        self.cursor_label.refresh()

    # running and close down of cursor flashing
    def flash_cursor(self):
        while self.typing:
            self.cursor_label.visible = not self.cursor_label.visible
            time.sleep(self.cursor_rate)

        self.cursor_active = False
        self.cursor_label.visible = False
