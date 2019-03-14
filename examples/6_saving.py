import sys, pygame
sys.path.append('..')

from util import *

class ExampleController(Controller):

    def __init__(self, interface):
        Controller.__init__(self, interface, debug=True)

    '''Initialize components and their attributes here
    '''
    def initialize_components(self):

        # create a panel to make a background color
        self.color_panel = Panel(self)
        self.color_panel.background = Color['blue']
        self.color_panel.width = self.screen_width
        self.color_panel.height = self.screen_height

        # create a text label
        self.hello_world_label = Label(self, 'Hello, World!')
        
        # create a button
        self.example_button = Button(self, 'Toggle Panel')
        self.example_button.action = self.toggle_color_panel
        self.example_button.anchor = self.example_button.center
        self.example_button.loc = self.screen_relative.center

        # press s to save
        Event(self, action=self.save_components, keys=(pygame.K_LCTRL, pygame.K_s,))
        # press l to load
        Event(self, action=self.load_components, keys=(pygame.K_LCTRL, pygame.K_l,))

    '''Example method to toggle the visibility of color panel
    '''
    def toggle_color_panel(self):
        self.color_panel.visible = not self.color_panel.visible

if __name__ ==  '__main__':
    interface = Interface()
    example = ExampleController(interface)
    example.run()
 