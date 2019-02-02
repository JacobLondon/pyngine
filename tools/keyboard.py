import pygame
from collections import defaultdict

class Keyboard(object):

    def __init__(self, controller):
        self.controller = controller

        self.typing = False
        self.shift = False
        self.typed_text = ''

        self.ignored_keys = [
            pygame.K_CAPSLOCK, pygame.K_LSHIFT, pygame.K_RSHIFT,
            pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_LALT, pygame.K_RALT,
            pygame.K_LSUPER, pygame.K_RSUPER, pygame.K_NUMLOCK, pygame.K_PRINT,
            pygame.K_SCROLLOCK, pygame.K_PAUSE, pygame.K_INSERT, pygame.K_HOME,
            pygame.K_PAGEUP, pygame.K_PAGEDOWN, pygame.K_DELETE, pygame.K_END,
            pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
            pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_F4, pygame.K_F5, pygame.K_F6,
            pygame.K_F7, pygame.K_F8, pygame.K_F9, pygame.K_F10, pygame.K_F11, pygame.K_F12]

        self.presses = defaultdict(lambda: False)

    def typing_actions(self, event):
        self.shift = self.presses[pygame.K_RSHIFT] or \
            self.presses[pygame.K_LSHIFT]

        # special keys
        if self.presses[pygame.K_BACKSPACE]:
            self.typed_text = self.typed_text[:-1]
        elif self.presses[pygame.K_TAB]:
            self.typed_text += ' ' * 4
        elif self.presses[pygame.K_RETURN]:
            self.typing = False
        elif self.presses[pygame.K_ESCAPE]:
            self.typing = False
        elif self.presses[pygame.K_SPACE]:
            self.typed_text += ' '

        elif self.shift:
            # shifted number keys
            if self.presses[pygame.K_1]:
                self.typed_text += '!'
            elif self.presses[pygame.K_2]:
                self.typed_text += '@'
            elif self.presses[pygame.K_3]:
                self.typed_text += '#'
            elif self.presses[pygame.K_4]:
                self.typed_text += '$'
            elif self.presses[pygame.K_5]:
                self.typed_text += '%'
            elif self.presses[pygame.K_6]:
                self.typed_text += '^'
            elif self.presses[pygame.K_7]:
                self.typed_text += '&'
            elif self.presses[pygame.K_8]:
                self.typed_text += '*'
            elif self.presses[pygame.K_9]:
                self.typed_text += '('
            elif self.presses[pygame.K_0]:
                self.typed_text += ')'

            # shifted letter keys
            elif pygame.key.name(event.key).isalpha():
                self.typed_text += pygame.key.name(event.key).upper()

            # misc shifted keys
            elif self.presses[pygame.K_BACKQUOTE]:
                self.typed_text += '~'
            elif self.presses[pygame.K_MINUS]:
                self.typed_text += '_'
            elif self.presses[pygame.K_EQUALS]:
                self.typed_text += '+'
            elif self.presses[pygame.K_LEFTBRACKET]:
                self.typed_text += '{'
            elif self.presses[pygame.K_RIGHTBRACKET]:
                self.typed_text += '}'
            elif self.presses[pygame.K_BACKSLASH]:
                self.typed_text += '|'
            elif self.presses[pygame.K_SEMICOLON]:
                self.typed_text += ':'
            elif self.presses[pygame.K_QUOTE]:
                self.typed_text += '"'
            elif self.presses[pygame.K_PERIOD]:
                self.typed_text += '<'
            elif self.presses[pygame.K_COMMA]:
                self.typed_text += '>'
            elif self.presses[pygame.K_SLASH]:
                self.typed_text += '?'

        # keypad keys
        elif self.presses[pygame.K_KP0]:
            self.typed_text += '0'
        elif self.presses[pygame.K_KP1]:
            self.typed_text += '1'
        elif self.presses[pygame.K_KP2]:
            self.typed_text += '2'
        elif self.presses[pygame.K_KP3]:
            self.typed_text += '3'
        elif self.presses[pygame.K_KP4]:
            self.typed_text += '4'
        elif self.presses[pygame.K_KP5]:
            self.typed_text += '5'
        elif self.presses[pygame.K_KP6]:
            self.typed_text += '6'
        elif self.presses[pygame.K_KP7]:
            self.typed_text += '7'
        elif self.presses[pygame.K_KP8]:
            self.typed_text += '8'
        elif self.presses[pygame.K_KP9]:
            self.typed_text += '9'
        elif self.presses[pygame.K_KP_PERIOD]:
            self.typed_text += '.'
        elif self.presses[pygame.K_KP_DIVIDE]:
            self.typed_text += '/'
        elif self.presses[pygame.K_KP_MULTIPLY]:
            self.typed_text += '*'
        elif self.presses[pygame.K_KP_MINUS]:
            self.typed_text += '-'
        elif self.presses[pygame.K_KP_PLUS]:
            self.typed_text += '+'
        elif self.presses[pygame.K_KP_ENTER]:
            self.typing = False
        elif self.presses[pygame.K_KP_EQUALS]:
            self.typed_text += '='

        elif event.key not in self.ignored_keys:
            self.typed_text += pygame.key.name(event.key)

     # do actions based on what was pressed
    def actions(self):

        self.custom_key_actions()

        if self.presses[pygame.K_RETURN]:
            self.return_keydown()
        if self.presses[pygame.K_ESCAPE]:
            self.escape_keydown()
        if self.presses[pygame.K_LEFT]:
            self.left_keydown()
        if self.presses[pygame.K_RIGHT]:
            self.right_keydown()
        if self.presses[pygame.K_UP]:
            self.up_keydown()
        if self.presses[pygame.K_DOWN]:
            self.down_keydown()

        if self.presses[pygame.K_w]:
            self.w_keydown()
        if self.presses[pygame.K_a]:
            self.a_keydown()
        if self.presses[pygame.K_s]:
            self.s_keydown()
        if self.presses[pygame.K_d]:
            self.d_keydown()
        if self.presses[pygame.K_SPACE]:
            self.space_keydown()
        if self.presses[pygame.K_LSHIFT]:
            self.lshift_keydown()

    # let the user define custom key checks
    def custom_key_actions(self):
        pass

    def return_keydown(self):
        pass
    def escape_keydown(self):
        pass
    def left_keydown(self):
        pass
    def right_keydown(self):
        pass
    def up_keydown(self):
        pass
    def down_keydown(self):
        pass

    def w_keydown(self):
        pass
    def a_keydown(self):
        pass
    def s_keydown(self):
        pass
    def d_keydown(self):
        pass
    def space_keydown(self):
        pass
    def lshift_keydown(self):
        pass