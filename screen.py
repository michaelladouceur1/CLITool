import curses
import math

''' Initialization of screen object and colors '''

curses_color_max = 1000
rgb_color_max = 255

def init_screen():
    screen = curses.initscr()
    curses.start_color()

    curses.curs_set(0)
    curses.mousemask(1)
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)

    h, w = screen.getmaxyx()

    return screen, h, w

def init_colors(screen,
    word_color,
    back_color,
    word_select_color,
    back_select_color,
    menu_color):
    
    # Default colors
    curses.init_color(1,*map_colors(word_color))
    curses.init_color(2,*map_colors(back_color))
    curses.init_pair(1,1,2)

    # Select colors
    curses.init_color(3,*map_colors(word_select_color))
    curses.init_color(4,*map_colors(back_select_color))
    curses.init_pair(2,3,4)

    # Menu colors
    curses.init_color(5,*map_colors(menu_color))
    curses.init_pair(3,5,2)

    screen.bkgd(' ', curses.color_pair(1))

def map_colors(color):
    return tuple(map(lambda x: math.ceil(x*(curses_color_max/rgb_color_max)), color))

def deinit_screen(screen):
    curses.curs_set(1)
    curses.mousemask(0)
    curses.echo()
    curses.nocbreak()
    screen.keypad(False)

    curses.endwin()