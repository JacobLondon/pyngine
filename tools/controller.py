import pygame, time, copy, re, time, collections
from threading import Thread, active_count as active_threads
from math import pi

from .panel import Panel
from .keyboard import Keyboard
from .mouse import Mouse

class Controller(object):

    def __init__(self, interface, tick_rate=1, clear=True, debug=False):

        self.debug = debug
        self.interface = interface
        if clear:
            self.interface.clear()
        
        self.update_time = time.time()
        self.delta_time = 0
        self.fps = 0
        self.tick_rate = tick_rate
        self.ticking = True     # ticking separate from framerate
        self.done = False       # controller looping
        self.quit = False       # close and return controller

        self.keyboard = Keyboard(self)
        self.mouse = Mouse(self)

        self.tick_thread = Thread(target=self.tick)

        # new technique for tracking components
        self.components = collections.OrderedDict()
        self.component_index = 0
        # depricated update method
        self.foreground_components = []
        self.background_components = []

        # create an empty panel for components to be on
        self.background_panel = Panel(self)
        self.background_panel.width = interface.resolution[0]
        self.background_panel.height = interface.resolution[1]
        self.background_panel.visible = False

    def initialize_components(self):
        pass

    ''' Tracking components
    '''
    def add(self, component, z=0):
        # append in next available index
        if z == 0:
            while self.component_index in self.components:
                self.component_index += 1
            self.components[self.component_index] = component
        # insert at given z index
        else:
            if z in self.components and self.debug:
                print('Warning: overriding component at z index:', z)
            self.components[z] = component

    def __str__(self):
        for z in self.components.keys():
            print('z = ', str(z), '\tComponent:', str(self.components[z]))

    ''' Updating components
    '''
    def draw(self):
        for key in self.components:
            self.components[key].refresh()

    def load(self):
        self.components = collections.OrderedDict(sorted(self.components.items(), reverse=True))
        for key in self.components:
            self.components[key].load()

    def elapsed_time(self):
        return time.time() - self.update_time

    # thread handling ticking
    def tick(self):
        while self.ticking:
            self.debug_actions()
            self.tick_actions()
            time.sleep(1 / self.tick_rate)

    def debug_actions(self):
        if self.debug:
            print('Threads:', active_threads())
            print('FPS:', self.fps)

    # custom actions during tick
    def tick_actions(self):
        pass

    def clear(self):
        self.interface.clear()

    # do on every frame
    def update(self):

        self.update_time = time.time()
        
        # if mouse is locked, reset it to locked position
        self.mouse.lock_update()

        # clear screen before drawing
        self.clear()
        self.draw()

        # pygame update
        self.interface.update()
        # track display stats
        self.delta_time = self.elapsed_time()
        self.fps = 1 / self.delta_time

    # do before the game loop, after component loading
    def setup(self):
        pass

    def stop(self):
        self.done = True

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
        # the close before running
        if self.done:
            self.open_on_close()

        self.initialize_components()
        self.load()
        
        self.setup()
        self.tick_thread.start()

        # loop over every frame
        while not self.done:
            t = Thread(target=self.update)
            t.start()

            self.keyboard.actions()
            self.mouse.actions()
            self.component_actions()

            # handle all events per frame
            for event in pygame.event.get():
                self.handle_event(event)
            
            t.join()

        return self.close()

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

    # actions for components
    def component_actions(self):
        pass

