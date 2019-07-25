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
        x_position = 'center',
        y_position = 'center',
        word_color = colors['white'],
        word_select_color = colors['charcoal'],
        back_color = colors['charcoal'],
        back_select_color = colors['white'],
        menu_color = colors['white']
        ):

        if not choices:
            raise ValueError('Choices can not be empty')
        # if not isinstance(y_position, int):
        #     raise ValueError('y_position can not be less than 0')
        # elif 
        # if x_position < 0:
        #     raise ValueError('x_position can not be less than 0')

        self.screen, self.h, self.w = init_screen()

        self.message = message
        self.set_message_height()
        self.choices = choices

        self.max_lines = max_lines
        self.x_position = x_position
        self.y_position = y_position
        self.set_prompt_boundaries()
        
        self.offset = 0
        self.selected = 0
        self.data = []

        self.word_color = word_color
        self.word_select_color = word_select_color
        self.back_color = back_color
        self.back_select_color = back_select_color
        self.menu_color = menu_color

        init_colors(
            self.screen,
            self.word_color, 
            self.back_color,
            self.word_select_color,
            self.back_select_color,
            self.menu_color)

    def set_prompt_boundaries(self):
        ''' Set prompt height '''
        if self.max_lines is not None:
            self.prompt_height = min(
                self.max_lines + self.message_height, 
                len(self.choices) + self.message_height, 
                self.h - 1)
        else:
            self.prompt_height = min(
                len(self.choices) + self.message_height, 
                self.h)

        ''' Set prompt top '''
        if self.y_position == 'center':
            self.prompt_top = self.h//2 - self.prompt_height//2
        elif self.y_position == 'top':
            self.prompt_top = 0
        elif isinstance(self.y_position, int):
            self.prompt_height -= self.y_position
            self.prompt_top = self.y_position

        ''' Set prompt bottom '''
        self.prompt_bottom = self.prompt_top + self.prompt_height

        ''' Set max lines for choices '''
        self.max_lines = self.prompt_height - self.message_height
        self.choices_top = self.prompt_top + self.message_height

    def set_message_height(self):
        self.message_height = 3 if self.message is not None else 0

    def orient_x(self, item):
        try:
            if self.x_position == 'center':
                x = self.w//2 - int(len(str(item))//2)
            elif self.x_position == 'left':
                x = 0
            elif isinstance(self.x_position, int):
                x = self.x_position
        except:
            print(f'x_position can not equal that')

        return x

    def orient_y(self, idx):
        return self.choices_top + idx

    def orient_message(self, x, y):
        mx = self.w//2 - int(len(self.message)//2)
        my = self.prompt_top

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
            self.screen.addstr(my+1,mx+1,f'({currentPage} of {totalPage})', curses.color_pair(3))
            rectangle(self.screen, my-1, mx-1, my+2, mx+len(self.message))
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
    choices=[f'PPC{random.randrange(100000)}.40' for i in range(100)], max_lines=10)
answer = select.run()
print(answer)