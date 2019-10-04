import curses
from curses.textpad import Textbox, rectangle

from colors import colors
from screen import deinit_screen
from component import Component


class Input(Component):

    def __init__(
        self,
        message = None,
        x_position = 'center',
        y_position = 'center',
        word_color = colors['defaultW'],
        word_select_color = colors['black'],
        back_color = colors['black'],
        back_select_color = colors['defaultSB'],
        message_color = colors['defaultW']
        ):

        super().__init__(
            message,
            word_color,
            word_select_color,
            back_color,
            back_select_color,
            message_color
        )

    def run(self):
        self.screen.addstr(1,1,self.message,curses.color_pair(3))
        self.screen.refresh()
        
        editwin = curses.newwin(1,30,1,len(self.message)+1)
        # self.screen.refresh()

        box = Textbox(editwin)
        box.edit()

        message = box.gather()

        deinit_screen(self.screen)

        return message

inp = Input(
    message='Enter a value: '
)
value = inp.run()
print(value)