import sys
import os
import curses

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from tetris import main

class Args:
    speed = 'medium'
    width = 10
    height = 20
    no_color = False
    seed = 123
    piece = None
    log = None
    auto = None
    no_shadow = False
    ghost = False

def run_test():
    try:
        curses.wrapper(main, Args())
    except Exception as e:
        import traceback
        with open('error.log', 'w') as f:
            traceback.print_exc(file=f)

if __name__ == '__main__':
    run_test()
