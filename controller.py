import pygame, time, copy, re
from threading import Thread, active_count as active_threads
from collections import defaultdict

from .constants import Mouse
from .panel import Panel

class Controller(object):

    def __init__(self, interface, tick_rate=1, clear=True):

        self.tick_rate = tick_rate
        self.ticking = True     # ticking separate from framerate
        self.done = False       # controller looping
        self.quit = False       # close and return controller

        self.typing = False     # user is typing text
        self.shift = False      # shift is being held while typing
        self.typed_text = ''    # the text the user is typing
        self.ignored_keys = [
            pygame.K_CAPSLOCK, pygame.K_LSHIFT, pygame.K_RSHIFT,
            pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_LALT, pygame.K_RALT,
            pygame.K_LSUPER, pygame.K_RSUPER, pygame.K_NUMLOCK, pygame.K_PRINT,
            pygame.K_SCROLLOCK, pygame.K_PAUSE, pygame.K_INSERT, pygame.K_HOME,
            pygame.K_PAGEUP, pygame.K_PAGEDOWN, pygame.K_DELETE, pygame.K_END,
            pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
            pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_F4, pygame.K_F5, pygame.K_F6,
            pygame.K_F7, pygame.K_F8, pygame.K_F9, pygame.K_F10, pygame.K_F11, pygame.K_F12]

        self.interface = interface
        if clear:
            self.interface.clear()

        self.key_presses = defaultdict(lambda: False)
        self.mouse_presses = defaultdict(lambda: False)
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.l_clicked_x, self.l_clicked_y = -1, -1
        self.m_clicked_x, self.m_clicked_y = -1, -1
        self.r_clicked_x, self.r_clicked_y = -1, -1

        self.tick_thread = Thread(target=self.tick)

        self.components = []

        # create an empty panel for components to be on
        self.background_panel = Panel(self)
        self.background_panel.width = interface.resolution[0]
        self.background_panel.height = interface.resolution[1]

    def initialize_components(self):
        pass

    def load_components(self):
        for component in self.components:
            component.load()

    # refresh/update components
    def update_components(self):
        for component in self.components:
            component.refresh()

    # thread handling ticking
    def tick(self):
        while self.ticking:
            print(active_threads())
            self.tick_actions()
            time.sleep(1 / self.tick_rate)

    # custom actions during tick
    def tick_actions(self):
        pass

    def clear(self):
        self.interface.clear()

    # do on every frame
    def update(self):

        # clear screen before drawing
        self.clear()
        self.draw_background()

        # custom component updates
        self.update_components()

        # draw and update controller items
        self.update_actions()

        # pygame update
        self.interface.update()

    # draw things behind all items
    def draw_background(self):
        pass

    # custom actions during update
    def update_actions(self):
        pass

    # do before the game loop, after component loading
    def setup(self):
        pass

    # the program will exit
    def close(self):
        self.ticking = False
        self.tick_thread.join()
        self.close_actions()

        # shutdown the program or open the parent container
        if self.quit:
            self.interface.close()
        else:
            self.open_on_close()

    # the controller will be closed
    def close_actions(self):
        pass

    # give the controller to run when the current one closes
    def open_on_close(self):

        # by default, close the program
        self.interface.close()

    # the program loop
    def run(self):

        # the connection failed before running
        if self.done:
            self.open_on_close()

        self.initialize_components()
        self.load_components()
        self.setup()
        self.tick_thread.start()

        # loop over every frame
        while not self.done:
            for event in pygame.event.get():
                self.handle_event(event)

            self.key_actions()
            self.mouse_actions()
            self.component_actions()
            Thread(target=self.update).start()

        return self.close()

    def handle_event(self, event):

        # top right corner X
        if event.type == pygame.QUIT:
            self.done = True
            self.quit = True

        # player starts doing actions
        elif event.type == pygame.KEYDOWN:
            self.key_presses[event.key] = True

        # player stops doing actions
        elif event.type == pygame.KEYUP:
            self.key_presses[event.key] = False

        # control user text input
        if self.typing and event.type == pygame.KEYDOWN:
            self.typing_actions(event)

        # mouse starts clicking/scrolling
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_presses[event.button] = True

        # mouse stops clicking/scrolling
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_presses[event.button] = False

        # mouse moves
        if event.type == pygame.MOUSEMOTION:
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

    # actions for components
    def component_actions(self):
        pass

    def typing_actions(self, event):

        self.shift = self.key_presses[pygame.K_RSHIFT] or \
            self.key_presses[pygame.K_LSHIFT]

        # special keys
        if self.key_presses[pygame.K_BACKSPACE]:
            self.typed_text = self.typed_text[:-1]
        elif self.key_presses[pygame.K_TAB]:
            self.typed_text += ' ' * 4
        elif self.key_presses[pygame.K_RETURN]:
            self.typing = False
        elif self.key_presses[pygame.K_ESCAPE]:
            self.typing = False
        elif self.key_presses[pygame.K_SPACE]:
            self.typed_text += ' '

        elif self.shift:
            # shifted number keys
            if self.key_presses[pygame.K_1]:
                self.typed_text += '!'
            elif self.key_presses[pygame.K_2]:
                self.typed_text += '@'
            elif self.key_presses[pygame.K_3]:
                self.typed_text += '#'
            elif self.key_presses[pygame.K_4]:
                self.typed_text += '$'
            elif self.key_presses[pygame.K_5]:
                self.typed_text += '%'
            elif self.key_presses[pygame.K_6]:
                self.typed_text += '^'
            elif self.key_presses[pygame.K_7]:
                self.typed_text += '&'
            elif self.key_presses[pygame.K_8]:
                self.typed_text += '*'
            elif self.key_presses[pygame.K_9]:
                self.typed_text += '('
            elif self.key_presses[pygame.K_0]:
                self.typed_text += ')'

            # shifted letter keys
            elif pygame.key.name(event.key).isalpha():
                self.typed_text += pygame.key.name(event.key).upper()

            # misc shifted keys
            elif self.key_presses[pygame.K_BACKQUOTE]:
                self.typed_text += '~'
            elif self.key_presses[pygame.K_MINUS]:
                self.typed_text += '_'
            elif self.key_presses[pygame.K_EQUALS]:
                self.typed_text += '+'
            elif self.key_presses[pygame.K_LEFTBRACKET]:
                self.typed_text += '{'
            elif self.key_presses[pygame.K_RIGHTBRACKET]:
                self.typed_text += '}'
            elif self.key_presses[pygame.K_BACKSLASH]:
                self.typed_text += '|'
            elif self.key_presses[pygame.K_SEMICOLON]:
                self.typed_text += ':'
            elif self.key_presses[pygame.K_QUOTE]:
                self.typed_text += '"'
            elif self.key_presses[pygame.K_PERIOD]:
                self.typed_text += '<'
            elif self.key_presses[pygame.K_COMMA]:
                self.typed_text += '>'
            elif self.key_presses[pygame.K_SLASH]:
                self.typed_text += '?'

        # keypad keys
        elif self.key_presses[pygame.K_KP0]:
            self.typed_text += '0'
        elif self.key_presses[pygame.K_KP1]:
            self.typed_text += '1'
        elif self.key_presses[pygame.K_KP2]:
            self.typed_text += '2'
        elif self.key_presses[pygame.K_KP3]:
            self.typed_text += '3'
        elif self.key_presses[pygame.K_KP4]:
            self.typed_text += '4'
        elif self.key_presses[pygame.K_KP5]:
            self.typed_text += '5'
        elif self.key_presses[pygame.K_KP6]:
            self.typed_text += '6'
        elif self.key_presses[pygame.K_KP7]:
            self.typed_text += '7'
        elif self.key_presses[pygame.K_KP8]:
            self.typed_text += '8'
        elif self.key_presses[pygame.K_KP9]:
            self.typed_text += '9'
        elif self.key_presses[pygame.K_KP_PERIOD]:
            self.typed_text += '.'
        elif self.key_presses[pygame.K_KP_DIVIDE]:
            self.typed_text += '/'
        elif self.key_presses[pygame.K_KP_MULTIPLY]:
            self.typed_text += '*'
        elif self.key_presses[pygame.K_KP_MINUS]:
            self.typed_text += '-'
        elif self.key_presses[pygame.K_KP_PLUS]:
            self.typed_text += '+'
        elif self.key_presses[pygame.K_KP_ENTER]:
            self.typing = False
        elif self.key_presses[pygame.K_KP_EQUALS]:
            self.typed_text += '='

        elif event.key not in self.ignored_keys:
            self.typed_text += pygame.key.name(event.key)

    def mouse_actions(self):
        if self.mouse_presses[Mouse.l_click]:
            self.l_clicked_x, self.l_clicked_y = pygame.mouse.get_pos()
            self.typing = copy.copy(self.background_panel.focused)
            self.l_click_down()
        if self.mouse_presses[Mouse.m_click]:
            self.m_clicked_x, self.m_clicked_y = pygame.mouse.get_pos()
            self.m_click_down()
        if self.mouse_presses[Mouse.r_click]:
            self.r_clicked_x, self.r_clicked_y = pygame.mouse.get_pos()
            self.r_click_down()
        if self.mouse_presses[Mouse.scroll_up]:
            self.scroll_up()
        if self.mouse_presses[Mouse.scroll_down]:
            self.scroll_down()

    def l_click_down(self):
        pass
    def m_click_down(self):
        pass
    def r_click_down(self):
        pass
    def scroll_up(self):
        pass
    def scroll_down(self):
        pass

    # do actions based on what was pressed
    def key_actions(self):

        self.custom_key_actions()

        if self.key_presses[pygame.K_RETURN]:
            self.return_keydown()
        if self.key_presses[pygame.K_ESCAPE]:
            self.escape_keydown()
        if self.key_presses[pygame.K_LEFT]:
            self.left_keydown()
        if self.key_presses[pygame.K_RIGHT]:
            self.right_keydown()
        if self.key_presses[pygame.K_UP]:
            self.up_keydown()
        if self.key_presses[pygame.K_DOWN]:
            self.down_keydown()

        if self.key_presses[pygame.K_w]:
            self.w_keydown()
        if self.key_presses[pygame.K_a]:
            self.a_keydown()
        if self.key_presses[pygame.K_s]:
            self.s_keydown()
        if self.key_presses[pygame.K_d]:
            self.d_keydown()

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
