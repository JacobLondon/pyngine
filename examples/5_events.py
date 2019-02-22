import sys, pygame
sys.path.append('..')

from tools import *

class ExampleController(Controller):

    def __init__(self, interface):
        Controller.__init__(self, interface, debug=True)

        # test number modification
        self.numbers = 0

    """Initialize components and their attributes here"""
    def initialize_components(self):
        
        self.inc_label = Label(self, 'press ctrl+up_arrow to increment')
        self.dec_label = Label(self, 'press lshift + down_arrow to decrement')
        self.dec_label.loc = self.screen_grid.get_pixel(0, 3)
        self.res_label = Label(self, 'press r to reset to zero')
        self.res_label.loc = self.screen_grid.get_pixel(0, 6)

        self.number_label = Label(self, str(self.numbers))
        self.number_label.loc = self.screen_relative.center
        self.number_label.anchor = self.number_label.center
        
        # events to do the custom actions
        Event(self, action=self.increase, keys=(pygame.K_LCTRL, pygame.K_UP,))
        Event(self, action=self.decrease, keys=(pygame.K_LSHIFT, pygame.K_DOWN,))
        Event(self, action=self.reset, keys=(pygame.K_r,))

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
    