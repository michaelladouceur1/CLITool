import curses
from curses.textpad import rectangle
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
        message_orient = 'top',
        choice_orient_x = 'center',
        choice_orient_y = 'center',
        word_color = colors.colors['defaultW'],
        word_select_color = colors.colors['black'],
        back_color = colors.colors['black'],
        back_select_color = colors.colors['defaultSB'],
        menu_color = colors.colors['defaultW']
        ):

        if not choices:
            raise ValueError('Choices can not be empty')
        if choice_orient_y < 0:
            raise ValueError('choice_orient_y can not be less than 0')
        if choice_orient_x < 0:
            raise ValueError('choice_orient_x can not be less than 0')

        self.init_screen()

        self.message = message
        self.message_height = 3
        self.choices = choices

        self.message_orient = message_orient
        self.choice_orient_x = choice_orient_x
        self.choice_orient_y = choice_orient_y

        if max_lines is not None:
            self.max_lines = max_lines
        else:
            self.max_lines = self.h

        if self.message is not None:
            self.prompt_height = self.max_lines + self.message_height
        else:
            self.prompt_height = self.max_lines

        if self.prompt_height > self.h:
            self.prompt_height = self.h
        

        # if self.message is not None:
        #     self.total_lines = max_lines + 2

        # if self.message is not None:
        #     if isinstance(choice_orient_y, int):
        #         self.max_lines = min(self.h-choice_orient_y, max_lines-choice_orient_y)
        #     else:
        #         self.max_lines = min(self.h, max_lines)
        # else:
        #     if isinstance(choice_orient_y, int):
        #         self.max_lines = min(self.h-choice_orient_y, max_lines-choice_orient_y)  
        #     else:
        #         self.max_lines = min(self.h, max_lines)

        self.offset = 0
        self.selected = 0
        self.data = []

        self.word_color = self.map_colors(word_color)
        self.word_select_color = self.map_colors(word_select_color)
        self.back_color = self.map_colors(back_color)
        self.back_select_color = self.map_colors(back_select_color)
        self.menu_color = self.map_colors(menu_color)

        self.init_colors(
            *self.word_color, 
            *self.back_color,
            *self.word_select_color,
            *self.back_select_color,
            *self.menu_color)

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
        r4,g4,b4,
        r5,g5,b5):
        
        # Default colors
        curses.init_color(1,r1,g1,b1)
        curses.init_color(2,r2,g2,b2)
        curses.init_pair(1,1,2)

        # Select colors
        curses.init_color(3,r3,g3,b3)
        curses.init_color(4,r4,g4,b4)
        curses.init_pair(2,3,4)

        # Menu colors
        curses.init_color(5,r5,g5,b5)
        curses.init_pair(3,5,2)

        self.screen.bkgd(' ', curses.color_pair(1))

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
            if self.choice_orient_x == 'center':
                x = self.w//2 - int(len(str(item))//2)
            elif self.choice_orient_x == 'left':
                x = 0
            elif isinstance(self.choice_orient_x, int):
                x = self.choice_orient_x
        except:
            print(f'choice_orient_x can not equal that')

        return x

    def orient_y(self, idx):
        try:
            if self.choice_orient_y == 'center':
                y = (self.h//2 - len(self.displayItems)//2) + idx
            elif self.choice_orient_y == 'top':
                y = idx
            elif isinstance(self.choice_orient_y, int):
                y = self.choice_orient_y + idx

            if self.message is not None and self.max_lines == self.h:
                self.max_lines -= 2
                y += 2 
        except:
            print(f'choice_orient_y can not equal that')

        self.data.append(y)

        return y

    def orient_message(self, x, y):
        if self.message_orient == 'top':
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
            totalPage = math.ceil(len(self.choices)/self.max_lines)
            currentPage = math.ceil(self.offset/self.max_lines) + 1
            self.screen.addstr(my,mx,f'{self.message} ({currentPage} of {totalPage})', curses.color_pair(3))
            self.screen.addstr(my+1,mx,'='*len(self.message), curses.color_pair(3))
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
            elif input == 10:
                self.deinit_screen()
                return self.choices[self.selected+self.offset]
            elif input == 27:
                self.deinit_screen()
                break
            else:
                pass

select = SSelect(
    message = 'PART NUMBER',
    choices=[f'PPC{random.randrange(100000)}.40' for i in range(1000)],
    menu_color=colors.colors['blue'], max_lines=15, choice_orient_y=5)
answer = select.run()
print(answer)

class MSelect:

    UP = 1
    DOWN = -1

    def __init__(
        self, 
        message = None,
        choices = [],
        max_lines = None,
        message_orient = 'top',
        choice_orient_x = 'center',
        choice_orient_y = 'center',
        word_color = colors.colors['defaultW'],
        word_select_color = colors.colors['black'],
        back_color = colors.colors['black'],
        back_select_color = colors.colors['defaultSB'],
        menu_color = colors.colors['defaultW']
        ):

        if not choices:
            raise ValueError('Choices can not be empty')

        self.init_screen()

        self.message = message
        self.choices = choices
        self.selectedChoices = []

        self.message_orient = message_orient
        self.choice_orient_x = choice_orient_x
        self.choice_orient_y = choice_orient_y

        if self.message is not None:
            if isinstance(choice_orient_y, int):
                self.max_lines = min(self.h-choice_orient_y, max_lines-choice_orient_y)

                if self.max_lines == self.h:
                    self.max_lines -= 2
                    self.choice_orient_y += 2
            else:
                self.max_lines = min(self.h, max_lines)

                if self.max_lines == self.h:
                    self.max_lines -= 2
                    self.choice_orient_y = 2
        else:
            if isinstance(choice_orient_y, int):
                self.max_lines = min(self.h-choice_orient_y, max_lines-choice_orient_y)  
            else:
                self.max_lines = min(self.h, max_lines)
        self.offset = 0
        self.selected = 0
        self.data = []

        self.word_color = self.map_colors(word_color)
        self.word_select_color = self.map_colors(word_select_color)
        self.back_color = self.map_colors(back_color)
        self.back_select_color = self.map_colors(back_select_color)
        self.menu_color = self.map_colors(menu_color)

        self.init_colors(
            *self.word_color, 
            *self.back_color,
            *self.word_select_color,
            *self.back_select_color,
            *self.menu_color)

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
        r4,g4,b4,
        r5,g5,b5):
        
        # Default colors
        curses.init_color(1,r1,g1,b1)
        curses.init_color(2,r2,g2,b2)
        curses.init_pair(1,1,2)

        # Select colors
        curses.init_color(3,r3,g3,b3)
        curses.init_color(4,r4,g4,b4)
        curses.init_pair(2,3,4)

        # Menu colors
        curses.init_color(5,r5,g5,b5)
        curses.init_pair(3,5,2)

        self.screen.bkgd(' ', curses.color_pair(1))

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
            if self.choice_orient_x == 'center':
                x = self.w//2 - int(len(str(item))//2)
            elif self.choice_orient_x == 'left':
                x = 0
            elif isinstance(self.choice_orient_x, int):
                x = self.choice_orient_x
        except:
            print(f'choice_orient_x can not equal that')

        return x

    def orient_y(self, idx):
        try:
            if self.choice_orient_y == 'center':
                y = (self.h//2 - len(self.displayItems)//2) + idx
            elif self.choice_orient_y == 'top':
                y = idx
            elif isinstance(self.choice_orient_y, int):
                y = self.choice_orient_y + idx

            if self.message is not None and self.max_lines == self.h:
                self.max_lines -= 2
                y += 2
        except:
            print(f'choice_orient_y can not equal that')

        self.data.append(y)

        return y

    def orient_message(self, x, y):
        mx = self.w//2 - int(len(self.message)//2)
        my = y - 3

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
            totalPage = math.ceil(len(self.choices)/self.max_lines)
            currentPage = math.ceil(self.offset/self.max_lines) + 1
            self.screen.addstr(my,mx,f'{self.message}', curses.color_pair(3))
            self.screen.addstr(my+1,mx,f'({currentPage} of {totalPage})', curses.color_pair(3))
            # self.screen.addstr(my+1,mx,'='*len(self.message), curses.color_pair(3))
            rectangle(self.screen, my-1, mx-1, my+2, mx+len(self.message))
        else:
            return


    def display(self, idx, item):
        x = self.orient_x(item)
        y = self.orient_y(idx)
        if idx == 0:
            self.display_message(x,y)

        if idx == self.selected or item in self.selectedChoices:
            self.screen.addstr(y,x,str(item),curses.color_pair(2))
        else:
            self.screen.addstr(y,x,str(item),curses.color_pair(1))

    def addChoice(self):
        item = self.choices[self.selected+self.offset]
        if item == any(self.selectedChoices):
            self.selectedChoices.remove(item)
        else:
            self.selectedChoices.append(item)

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
            elif input == 10:
                self.deinit_screen()
                return self.selectedChoices
            elif input == 32:
                self.addChoice()
            elif input == 27:
                self.deinit_screen()
                break
            else:
                pass

# select = MSelect(
#     message = 'PART NUMBER',
#     choices=[f'PPC{random.randrange(100000)}.40' for i in range(1000)],
#     menu_color=colors.colors['blue'], max_lines=15, choice_orient_y=5)
# answer = select.run()
# print(answer)