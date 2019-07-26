from screen import init_screen, init_colors, deinit_screen
from colors import colors

''' Root Component class that all components inherit '''

class Component():

    def __init__(
        self,
        message = None,
        word_color = colors['white'],
        word_select_color = colors['charcoal'],
        back_color = colors['charcoal'],
        back_select_color = colors['white'],
        message_color = colors['white']
        ):

        self.screen, self.h, self.w = init_screen()

        self.message = message
        self.set_message_height()

        self.word_color = word_color
        self.word_select_color = word_select_color
        self.back_color = back_color
        self.back_select_color = back_select_color
        self.message_color = message_color

        init_colors(
            self.screen,
            self.word_color, 
            self.back_color,
            self.word_select_color,
            self.back_select_color,
            self.message_color)

    def set_message_height(self):
        self.message_height = 3 if self.message is not None else 0