import curses
from curses.textpad import rectangle
import time
import math
import random
from colors import colors
from screen import init_screen, init_colors, deinit_screen

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
        word_color = colors['defaultW'],
        word_select_color = colors['black'],
        back_color = colors['black'],
        back_select_color = colors['defaultSB'],
        menu_color = colors['defaultW']
        ):

        if not choices:
            raise ValueError('Choices can not be empty')
        # if choice_orient_y < 0:
        #     raise ValueError('choice_orient_y can not be less than 0')
        # if choice_orient_x < 0:
        #     raise ValueError('choice_orient_x can not be less than 0')

        self.screen, self.h, self.w = init_screen()

        self.message = message
        self.set_message_height()
        self.choices = choices

        self.max_lines = max_lines
        self.message_orient = message_orient
        self.choice_orient_x = choice_orient_x
        self.choice_orient_y = choice_orient_y
        self.set_prompt_boundaries()
        
        self.offset = 0
        self.selected = 0
        self.data = []

        self.word_color = self.map_colors(word_color)
        self.word_select_color = self.map_colors(word_select_color)
        self.back_color = self.map_colors(back_color)
        self.back_select_color = self.map_colors(back_select_color)
        self.menu_color = self.map_colors(menu_color)

        init_colors(
            self.screen,
            *self.word_color, 
            *self.back_color,
            *self.word_select_color,
            *self.back_select_color,
            *self.menu_color)

    def map_colors(self,color):
        return tuple(map(lambda x: math.ceil(x*3.92156), color))

    def set_prompt_boundaries(self):
        # PROMPT HEIGHT
        if self.max_lines is not None:
            self.prompt_height = min(self.max_lines + self.message_height, len(self.choices) + self.message_height, self.h)
        else:
            self.prompt_height = min(len(self.choices) + self.message_height, self.h)

        # PROMPT TOP
        if self.choice_orient_y == 'center':
            self.prompt_top = self.h//2 - self.prompt_height//2
        elif self.choice_orient_y == 'top':
            self.prompt_top = 0
        elif isinstance(self.choice_orient_y, int):
            self.prompt_height -= self.choice_orient_y
            self.prompt_top = self.choice_orient_y

        # PROMPT BOTTOM
        self.prompt_bottom = self.prompt_top + self.prompt_height

    # def validate_prompt_boundaries(self):
    #     if self.prompt_top < 0:


    def set_message_height(self):
        if self.message is not None:
            self.message_height = 3
        else:
            self.message_height = 0

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
                deinit_screen(self.screen)
                return self.choices[self.selected+self.offset]
            elif input == 27:
                deinit_screen(self.screen)
                break
            else:
                pass

select = SSelect(
    message = 'PART NUMBER',
    choices=[f'PPC{random.randrange(100000)}.40' for i in range(1000)],
    menu_color=colors['green'], back_select_color=colors['yellow'], max_lines=15)
answer = select.run()
print(answer)

select = SSelect(
    message = 'ASSEMBLY NUMBER',
    choices=[f'PPC{random.randrange(100000)}.40' for i in range(1000)],
    menu_color=colors['green'], back_select_color=colors['blue'], max_lines=15, choice_orient_y=5)
answer = select.run()
print(answer)