import curses
from curses.textpad import rectangle
import math
from screen import init_screen, init_colors, deinit_screen
from colors import colors

''' Root Component class that all components inherit '''

class Component():

    def __init__(
        self,
        message,
        word_color,
        word_select_color,
        back_color,
        back_select_color,
        message_color
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

class ListComponent(Component):

    def __init__(
        self,
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
        ):

        super().__init__(
            message,
            word_color,
            word_select_color,
            back_color,
            back_select_color,
            message_color
        )

        if not choices:
            raise ValueError('Choices can not be empty')

        self.choices = choices

        self.max_lines = max_lines
        self.x_position = x_position
        self.y_position = y_position
        self.set_prompt_boundaries()

        self.offset = 0
        self.selected = 0

    def class_attributes(cls):
        print(f'{cls.__dict__}\n\n')
        return True if 'selectedChoices' in cls.__dict__ else False

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
                self.h - 1)

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

    def display(self, idx, item):
        x = self.orient_x(item)
        y = self.orient_y(idx)
        if idx == 0:
            self.display_message(x,y)

        if self.class_attributes() == True:
            if idx == self.selected or item in self.selectedChoices:
                self.screen.addstr(y,x,str(item),curses.color_pair(2))
            else:
                self.screen.addstr(y,x,str(item),curses.color_pair(1))
        else:
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