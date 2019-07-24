import curses

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

    screen.bkgd(' ', curses.color_pair(1))

def deinit_screen(screen):
    curses.curs_set(1)
    curses.mousemask(0)
    curses.echo()
    curses.nocbreak()
    screen.keypad(False)

    curses.endwin()