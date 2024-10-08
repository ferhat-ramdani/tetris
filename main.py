import time
import curses

stdscr = curses.initscr()

def main(stdscr):
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    draw_termtris(stdscr, 'a', 3, 3)
    draw_termtris(stdscr, 'b', 3, 15)
    stdscr.refresh()
    time.sleep(3)

    curses.curs_set(1)
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(False)

def draw_termtris(stdscr, piece: str, x: int, y: int):
    file = open(f"pieces/{piece}.txt", 'r')
    lines = [line.rstrip() for line in file]
    for l_index, line in enumerate(lines):
        for c_index, c in enumerate(line) :
            stdscr.addstr(l_index + y, x + c_index, c)

curses.wrapper(main)