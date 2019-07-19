# import curses
# import time
import math

# screen = curses.initscr()
# curses.start_color()

# curses.curs_set(0)
# curses.noecho()
# curses.cbreak()
# screen.keypad(True)

# # curses.init_color(1,0,0,0)
# # curses.init_color(2,1000,1000,1000)

# # curses.init_pair(1, 1, 2)

# screen.addstr(0,0,'HELLOOOO', curses.color_pair(1))
# screen.refresh()
# time.sleep(5)


# curses.curs_set(1)
# curses.echo()
# curses.nocbreak()
# screen.keypad(False)

# curses.endwin()

# colors = {
# 	'black'	: (0,0,0),
# 	'white' : (1000,1000,1000)
# }

# def init_colors(r,g,b):
# 	curses.init_color(1,r,g,b)
# 	curses.init_color(2,1000,1000,1000)

# 	return curses.init_pair(1,1,2)

# init_color(*colors['black'])


import curses 

# screen = curses.initscr() 
# #curses.noecho() 
# curses.curs_set(0) 
# screen.keypad(1) 
# curses.mousemask(1)

# screen.addstr("This is a Sample Curses Script\n\n") 

# while True:
#     event = screen.getch() 
#     if event == ord("q"): break 
#     if curses.BUTTON1_DOUBLE_CLICKED:
#         ids, mx, my, mz, b = curses.getmouse()
#         y, x = screen.getyx()
#         screen.addstr(my, mx, f'{ids}: {mx} & {my}\t')
#         screen.refresh()

# curses.endwin()

screen = curses.initscr()

curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

if x == 0:
	starty, startx = screen.getmaxyx()
	x = startx
	y = starty
	
resize = curses.is_term_resized(y, x)

# Action in loop if resize is True:
if resize is True:
	y, x = screen.getmaxyx()
	screen.clear()
	curses.resizeterm(y, x)
	screen.refresh()


# show_header()
