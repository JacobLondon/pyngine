import sys
sys.path.append('..')

from tools import *

class ExampleController(Controller):

    def __init__(self, interface):
        Controller.__init__(self, interface, debug=True)
        self.keyboard.return_keydown = self.test

    '''Initialize components and their attributes here
    '''
    def initialize_components(self):
        
        self.text = Textbox(self)

    def test(self):
        print('test')

if __name__ == '__main__':
    interface = Interface()
    example = ExampleController(interface)
    example.run()
    