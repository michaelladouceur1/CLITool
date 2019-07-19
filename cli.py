import curses
import time

class SSelect:
    def __init__(
        self, 
        message = '',
        choices = [],
        message_orient = 'TOP',
        choice_orient_x = 'CENTER',
        choice_orient_y = 'CENTER',
        word_color = curses.COLOR_WHITE,
        word_select_color = curses.COLOR_BLACK,
        back_color = curses.COLOR_BLACK,
        back_select_color = curses.COLOR_WHITE
        ):

        if not choices:
            raise ValueError('Choices can not be empty')

        self.init_screen()

        self.message = message
        self.choices = choices

        self.message_orient = message_orient
        self.choice_orient_x = choice_orient_x
        self.choice_orient_y = choice_orient_y

        self.word_color = word_color
        self.word_select_color = word_select_color
        self.back_color = back_color
        self.back_select_color = back_select_color

    def init_screen(self):
        self.screen = curses.initscr()

        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)

        self.h, self.w = self.screen.getmaxyx()

    def deinit_screen(self):
        curses.curs_set(1)
        curses.echo()
        curses.nocbreak()
        self.screen.keypad(False)

        curses.endwin()

    def orient_x(self, item):
        try:
            if self.choice_orient_x == 'CENTER':
                x = self.w//2 - len(item)//2
            elif self.choice_orient_x == 'LEFT':
                x = 0
        except:
            print(f'choice_orient_x can not equal that')

        return x

    def orient_y(self, idx):
        try:
            if self.choice_orient_y == 'CENTER':
                y = (self.h//2 - len(self.choices)//2) + idx
            elif self.choice_orient_y == 'TOP':
                y = idx
        except:
            print(f'choice_orient_y can not equal that')

        return y

    def display(self, idx, item):
        print('display called')
        x = self.orient_x(item)
        y = self.orient_y(idx)
        self.screen.addstr(y,x,item)

    def render(self):
        print('render called')
        for idx, item in enumerate(self.choices):
            self.display(idx, item)
        self.screen.refresh()
        time.sleep(5)

select = SSelect(choices=['Hello', 'Goodbye', 'Maybe', 'Definitely Not', 'Yes', 'No'], choice_orient_y='TOP')
select.render()
select.deinit_screen()