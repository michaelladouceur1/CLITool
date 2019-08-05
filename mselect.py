import curses
from curses.textpad import rectangle
import time
import math
import random
from colors import colors
from screen import init_screen, init_colors, deinit_screen
from component import Component, ListComponent


class MSelect(ListComponent):

    UP = 1
    DOWN = -1

    def __init__(
        self, 
        message = None,
        choices = [],
        max_lines = None,
        message_orient = 'top',
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

        self.selectedChoices = []

    def addChoice(self):
        item = self.choices[self.selected+self.offset]
        self.selectedChoices.remove(item) if item in self.selectedChoices else self.selectedChoices.append(item)

    def run(self):

        while True:
            self.render()

            input = self.screen.getch()
            if input == curses.KEY_UP:
                self.scroll(self.UP)
            elif input == curses.KEY_DOWN:
                self.scroll(self.DOWN)
            elif input == curses.KEY_RIGHT:
                self.page(self.DOWN)
            elif input == curses.KEY_LEFT:
                self.page(self.UP)
            elif input == 10:
                if len(self.selectedChoices) > 0:
                    deinit_screen(self.screen)
                    return self.selectedChoices
                else:
                    pass
            elif input == 32:
                self.addChoice()
            elif input == 27:
                deinit_screen(self.screen)
                break
            else:
                pass

select = MSelect(
    message = 'PART NUMBER',
    choices=[f'PPC{random.randrange(100000)}.40' for i in range(50)],
    message_color=colors['blue'], max_lines=15, y_position=5)
answer = select.run()
print(answer)