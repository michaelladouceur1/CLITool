import curses
import time
import math
import random
import colors

class SSelect:

    UP = 1
    DOWN = -1

    def __init__(
        self, 
        message = None,
        choices = [],
        max_lines = None,
        message_orient = 'TOP',
        choice_orient_x = 'CENTER',
        choice_orient_y = 'CENTER',
        word_color = colors.colors['defaultW'],
        word_select_color = colors.colors['black'],
        back_color = colors.colors['black'],
        back_select_color = colors.colors['defaultSB']
        ):

        if not choices:
            raise ValueError('Choices can not be empty')

        self.init_screen()

        self.message = message
        self.choices = choices
        self.max_lines = min(self.h, max_lines)
        self.offset = 0
        self.selected = 0

        self.message_orient = message_orient
        self.choice_orient_x = choice_orient_x
        self.choice_orient_y = choice_orient_y

        self.word_color = self.map_colors(word_color)
        self.word_select_color = self.map_colors(word_select_color)
        self.back_color = self.map_colors(back_color)
        self.back_select_color = self.map_colors(back_select_color)

        self.init_colors(
            *self.word_color, 
            *self.back_color,
            *self.word_select_color,
            *self.back_select_color)

    def init_screen(self):
        self.screen = curses.initscr()
        curses.start_color()

        curses.curs_set(0)
        curses.mousemask(1)
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)

        self.h, self.w = self.screen.getmaxyx()

    def init_colors(self,
        r1,g1,b1,
        r2,g2,b2,
        r3,g3,b3,
        r4,g4,b4):
        
        # Display colors
        curses.init_color(1,r1,g1,b1)
        curses.init_color(2,r2,g2,b2)
        curses.init_pair(1,1,2)

        # Select colors
        curses.init_color(3,r3,g3,b3)
        curses.init_color(4,r4,g4,b4)
        curses.init_pair(2,3,4)

    def map_colors(self,color):
        return tuple(map(lambda x: math.ceil(x*3.92156), color))

    def deinit_screen(self):
        curses.curs_set(1)
        curses.mousemask(0)
        curses.echo()
        curses.nocbreak()
        self.screen.keypad(False)

        curses.endwin()

    def orient_x(self, item):
        try:
            if self.choice_orient_x == 'CENTER':
                x = self.w//2 - int(len(str(item))//2)
            elif self.choice_orient_x == 'LEFT':
                x = 0
        except:
            print(f'choice_orient_x can not equal that')

        return x

    def orient_y(self, idx):
        try:
            if self.choice_orient_y == 'CENTER':
                y = (self.h//2 - len(self.displayItems)//2) + idx
            elif self.choice_orient_y == 'TOP':
                y = idx
        except:
            print(f'choice_orient_y can not equal that')

        return y

    def orient_message(self, x, y):
        if self.message_orient == 'TOP':
            mx = self.w//2 - int(len(self.message)//2)
            my = y - 2

        return mx, my

    def scroll(self, direction):
        if self.selected == 0 and direction == self.UP:
            self.selected = len(self.displayItems) - 1
        elif self.selected == len(self.displayItems) - 1 and direction == self.DOWN:
            self.selected = 0
        else:
            self.selected -= direction

    def page(self, direction):
        offTest = self.offset
        if direction == self.UP:
            offTest -= self.max_lines
        elif direction == self.DOWN:
            offTest += self.max_lines
        else:
            return

        if 0 <= offTest < len(self.choices):
            self.offset = offTest
        else:
            return
    
    def display_message(self, x, y):
        if self.message is not None:
            mx, my = self.orient_message(x, y)
            self.screen.addstr(my,mx,self.message, curses.color_pair(1))
            self.screen.addstr(my+1,mx,'='*len(self.message), curses.color_pair(1))
        else:
            return


    def display(self, idx, item):
        x = self.orient_x(item)
        y = self.orient_y(idx)
        if idx == 0:
            self.display_message(x,y)

        if idx == self.selected:
            self.screen.addstr(y,x,str(item),curses.color_pair(2))
        else:
            self.screen.addstr(y,x,str(item),curses.color_pair(1))

    def render(self):
        self.screen.erase()
        if self.max_lines is not None:
            self.displayItems = self.choices[self.offset:(self.max_lines+self.offset)]
        else:
            self.displayItems = self.choices

        for idx, item in enumerate(self.displayItems):
            self.display(idx, item)
        self.screen.refresh()

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
            elif input == 10 or 459:
                return self.choices[self.selected+self.offset]
            elif input == 27:
                break

select = SSelect(
    message = 'MAIN MENU',
    choices=[x for x in range(0,100)],
    word_color=(144, 252, 202), max_lines=20)
answer = select.run()
print(answer)
select.deinit_screen()