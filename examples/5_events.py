import sys, pygame
sys.path.append('..')

from tools import *

class ExampleController(Controller):

    def __init__(self, interface):
        Controller.__init__(self, interface, debug=False)

        # test number modification
        self.numbers = 0

    """Initialize components and their attributes here"""
    def initialize_components(self):
        
        self.inc_label = Label(self, 'press ctrl+up_arrow to increment')
        self.dec_label = Label(self, 'press lshift + down_arrow to decrement')
        self.dec_label.loc = self.screen_grid.get_pixel(0, 1)
        self.res_label = Label(self, 'press r to reset to zero')
        self.res_label.loc = self.screen_grid.get_pixel(0, 2)

        self.number_label = Label(self, str(self.numbers))
        self.number_label.loc = self.screen_relative.center
        self.number_label.anchor = self.number_label.center
        
        # events to do the custom actions
        Event(self, key=(pygame.K_LCTRL, pygame.K_UP,), action=self.increase)
        Event(self, key=(pygame.K_LSHIFT, pygame.K_DOWN,), action=self.decrease)
        Event(self, key=(pygame.K_r,), action=self.reset)

    def increase(self):
        self.numbers += 1
        self.number_label.text = str(self.numbers)
        
    def decrease(self):
        self.numbers -= 1
        self.number_label.text = str(self.numbers)

    def reset(self):
        self.numbers = 0
        self.number_label.text = str(self.numbers)

if __name__ == '__main__':
    interface = Interface()
    example = ExampleController(interface)
    example.run()
    