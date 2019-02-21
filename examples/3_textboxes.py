import sys
sys.path.append('..')
import pygame

from tools import *

class ExampleController(Controller):

    def __init__(self, interface):
        Controller.__init__(self, interface, debug=True)

    """Initialize components and their attributes here"""
    def initialize_components(self):
        
        self.text = Textbox(self)

        #self.test_event = Event(controller=self, key=pygame.K_ESCAPE, action=self.test)

    def test(self):
        print('test')

if __name__ == '__main__':
    interface = Interface()
    example = ExampleController(interface)
    example.run()
    