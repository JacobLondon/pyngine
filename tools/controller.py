import pygame, time, copy, re, time, collections
from threading import Thread, active_count as active_threads
from math import pi

from .event import Event
from .graphics import Painter, Color
from .gui import Panel, Grid, Relative
from .keyboard import Keyboard
from .mouse import Mouse

"""Handle drawing things to screen and user input from mouse/keyboard.

This class is meant to be extended for simple functionality.
"""
class Controller(object):

    def __init__(self, interface, tick_rate=1, clear=True, debug=False):

        # pygame interface with controller
        self.interface = interface
        if clear:
            self.interface.clear()

        self.screen_width = self.interface.resolution[0]
        self.screen_height = self.interface.resolution[1]

        # interface with pygame to draw shapes/lines/areas
        self.painter = Painter(self.interface)
        
        # tools for tracking fps/time to update
        self.update_time = time.time()
        self.delta_time = 0
        self.fps = 0

        # close the controller
        self.done = False
        # close pygame and the display
        self.quit = False

        # control input
        self.keyboard = Keyboard(self)
        self.mouse = Mouse(self)
        self.events = {}

        # do regularly in a different thread
        self.tick_thread = Thread(target=self.tick)
        self.tick_rate = tick_rate
        self.ticking = True
        self.debug = debug

        # load/refresh components/drawers based on their z index
        self.components = collections.OrderedDict()
        self.component_index = 0

        # create an empty panel for components to be on
        self.background_panel = Panel(self)
        self.background_panel.width = interface.resolution[0]
        self.background_panel.height = interface.resolution[1]
        self.background_panel.background = Color['gray5']

        # create default screen layouts based on background panel
        self.screen_grid = Grid(self.background_panel, self.interface.tile_width, self.interface.tile_height)
        self.screen_relative = Relative(self.background_panel)

        # clear is the same as interface's clear
        self.clear = self.interface.clear

    """Get the component.text and its z index for all components"""
    def __str__(self):
        for z in self.components.keys():
            print('z = ', str(z), '\tComponent:', str(self.components[z]))

    """Initialize components after run() is called on the controller."""
    def initialize_components(self):
        pass

    """Add components to the OrderedDict of components based on their z index"""
    def add_component(self, component, z=0):
        # no z index given
        if z == 0:
            # append in next available index
            while self.component_index in self.components:
                self.component_index += 1
            self.components[self.component_index] = component
        # insert at given z index
        else:
            if z in self.components:
                print('Warning: overriding component at z index:', z)
            self.components[z] = component

    """Add an event specified by a key and an action function"""
    def add_event(self, event):
        self.events[event.key] = event

    """Call all events specified by the user the they are occurring"""
    def call_events(self):
        for key in self.events.keys():
            if self.keyboard.presses[key] or self.mouse.presses[key]:
                self.events[key].action()

    """Draw all components to screen in their z index order"""
    def draw(self):
        for key in self.components:
            self.components[key].refresh()

    """Load components before entering program loop to ensure z index order is correct"""
    def load(self):
        self.components = collections.OrderedDict(sorted(self.components.items(), reverse=False))
        for key in self.components:
            self.components[key].load()

    """Tick in another thread to handle custom ticking actions and debug messages"""
    def tick(self):
        while self.ticking:
            self.debug_actions()
            self.tick_actions()
            time.sleep(1 / self.tick_rate)

    """Show thread count and frames per second"""
    def debug_actions(self):
        if self.debug:
            print('Threads:', active_threads())
            print('FPS:', self.fps)

    """Empty method meant to be overwritten by controller children"""
    def tick_actions(self):
        pass

    """Do every frame in another thread from input"""
    def update(self):
        
        # if mouse is locked, reset it to locked position
        self.mouse.lock_update()

        # clear screen before drawing
        self.clear()
        self.draw()

        # pygame update
        self.interface.update()

        # record update
        self.delta_time = self.elapsed_time()
        self.update_time = time.time()
        self.fps = 1 / self.delta_time

    """Find how much time has passed since the last update"""
    def elapsed_time(self):
        t = time.time() - self.update_time
        # make sure that t is not zero, prevent div by zero
        return t if not t == 0 else self.delta_time

    """Do before the program loop,
    but after components have been loaded
    """
    def setup(self):
        pass

    """Method for stopping the program loop"""
    def stop(self):
        self.done = True

    """Handle closing the controller by
    stopping threads, doing custom close actions,
    and opening another controller if given
    """
    def close(self):
        # close actions
        self.ticking = False
        self.tick_thread.join()
        # custom close actions
        self.close_actions()

        # shutdown the program or open the parent container
        if self.quit:
            self.interface.close()
        else:
            self.open_on_close()

    """Custom actions to do when the controller is closing
    Meant to be overwritten by controller children
    """
    def close_actions(self):
        pass

    """Stop the program by default.
    Override in child by importing a controller and running it here
    """
    def open_on_close(self):

        # by default, close the program
        self.interface.close()

    """The program loop
    Includes pre-program loop actions, the loop, and updating
    """
    def run(self):
        # if the controller loading was cancelled before opening
        if self.done:
            self.open_on_close()

        # pre-program loop actions
        self.initialize_components()
        self.load()
        self.setup()
        self.tick_thread.start()

        # the program loop
        while not self.done:

            # update in another thread
            t = Thread(target=self.update)
            t.start()

            # receive keyboard/mouse input
            self.keyboard.actions()
            self.mouse.actions()
            #TODO
            #self.call_events()
            #print(self.events)

            # custom actions defined by child
            self.custom_actions()

            # handle all events per frame
            for event in pygame.event.get():
                self.handle_event(event)
            
            # ensure the updating has finished
            t.join()

        # close the controller and handle close actions
        self.close()
 
    """Custom actions done every frame
    Meant to be overwritten by controller children
    """
    def custom_actions(self):
        pass

    """Given a pygame event, record it in its
    respective mouse/keyboard presses DefaultDict.
    This dict determines pressing state for each key/button.
    """
    def handle_event(self, event):

        # top right corner X
        if event.type == pygame.QUIT:
            self.done = True
            self.quit = True

        # player starts doing actions
        elif event.type == pygame.KEYDOWN:
            self.keyboard.presses[event.key] = True

        # player stops doing actions
        elif event.type == pygame.KEYUP:
            self.keyboard.presses[event.key] = False

        # control user text input
        if self.keyboard.typing and event.type == pygame.KEYDOWN:
            self.keyboard.typing_actions(event)

        # mouse stops clicking/scrolling
        if event.type == pygame.MOUSEBUTTONUP:
            if not event.button == Mouse.scroll_up \
                and not event.button == Mouse.scroll_down:
                self.mouse.presses[event.button] = False

        # mouse starts clicking/scrolling
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse.presses[event.button] = True

        # mouse moves
        if event.type == pygame.MOUSEMOTION:
            self.mouse.motion_update()
