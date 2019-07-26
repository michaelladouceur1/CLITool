

# import curses
# from curses.textpad import Textbox, rectangle
# from curses import wrapper

# def main(stdscr):
# 	stdscr.addstr(0, 0, "Enter IM message: (hit Ctrl-G to send)")

# 	editwin = curses.newwin(5,30, 0,40)
# 	# stdscr.subpad(10,10,0,0)
# 	# rectangle(stdscr, 1,0, 1+5+1, 1+30+1)
# 	stdscr.refresh()

# 	box = Textbox(editwin)

# 	# Let the user edit until Ctrl-G is struck.
# 	box.edit()

# 	# Get resulting contents
# 	message = box.gather()

# 	return message

# mess = wrapper(main)

# print(mess)

from bullet import SlidePrompt, YesNo, Input, Numbers, Bullet

cli = SlidePrompt(
    [
        YesNo("Are you a student? "),
        Input("Who are you? "),
        Numbers("How old are you? "),
        Bullet("What is your favorite programming language? ",
              choices = ["C++", "Python", "Javascript", "Not here!"]),
    ]
)

result = cli.launch()
print(result)