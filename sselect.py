import curses
from curses.textpad import rectangle
import time
import math
import random
from colors import colors
from screen import init_screen, init_colors, deinit_screen
from component import Component, ListComponent

''' Single Selection Component: Select one item from choices to return '''

class SSelect(ListComponent):

    UP = 1
    DOWN = -1

    def __init__(
        self, 
        message = None,
        choices = [],
        max_lines = None,
        x_position = 'center',
        y_position = 'center',
        word_color = colors['white'],
        word_select_color = colors['charcoal'],
        back_color = colors['charcoal'],
        back_select_color = colors['white'],
        message_color = colors['white']
        ):

        super().__init__(
            message,
            choices,
            max_lines,
            x_position,
            y_position,
            word_color, 
            word_select_color, 
            back_color, 
            back_select_color, 
            message_color
            )

    def run(self):

        while True:
            self.render()

            input = self.screen.getch()
            if input == curses.KEY_UP:
                self.scroll(self.UP)
            elif input == curses.KEY_DOWN:
                self.scroll(self.DOWN)
            elif input == curses.KEY_RIGHT or input == 338:
                self.page(self.DOWN)
            elif input == curses.KEY_LEFT or input == 339:
                self.page(self.UP)
            elif input == 10:
                deinit_screen(self.screen)
                return self.choices[self.selected+self.offset]
            elif input == 27:
                deinit_screen(self.screen)
                break
            else:
                pass

select = SSelect(
    message = 'PART NUMBER',
    choices=[f'PPC{random.randrange(100000)}.40' for i in range(100)], y_position=5, max_lines=12)
answer = select.run()
print(answer)

select = SSelect(
    message = 'PART NUMBER',
    choices=[f'PPC{random.randrange(100000)}.40' for i in range(100)], y_position=5, max_lines=12)
answer = select.run()
print(answer)

