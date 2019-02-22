import sys
sys.path.append('..')

from tools import *

class ExampleController(Controller):

    def __init__(self, interface):
        Controller.__init__(self, interface, debug=False)

    """Initialize components and their attributes here"""
    def initialize_components(self):
        
        self.test_textbox = Textbox(self)
        self.test_textbox.loc = self.screen_relative.center
        self.test_textbox.anchor = self.test_textbox.center

if __name__ == '__main__':
    interface = Interface()
    example = ExampleController(interface)
    example.run()
    