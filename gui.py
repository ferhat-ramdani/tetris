
import curses
import time

from grid import *


def draw_piece(window, piece, start_y, start_x):
  for y, row in enumerate(piece):
    for x, char in enumerate(row):
      if char == 'x':
        window.addch(start_y + y, start_x + x, char)

def draw_grid(window, grid, margin=1):
  for y, row in enumerate(grid):
    for x, char in enumerate(row):
      window.addch(y + margin, x + margin, char)


def draw_borders(window, cols, rows) :
  for x in range(cols + 2):
    window.addch(0, x, '-')
    window.addch(rows + 1, x, '-')
  for y in range(rows + 2):
    window.addch(y, 0, '|')
    window.addch(y, cols + 1, '|')

def handle_key_events(window, position, random_piece, grid, cols, rows):
  start_time = time.time()
  while time.time() - start_time < 1:
    key = window.getch()
    window.timeout(1000)
    if key == curses.KEY_LEFT and can_move(grid, random_piece, tuple(position), 'l'):
      remove_piece(grid, random_piece, tuple(position))
      position[1] -= 1
      put_piece(grid, random_piece, tuple(position))
    elif key == curses.KEY_RIGHT and can_move(grid, random_piece, tuple(position), 'r'):
      remove_piece(grid, random_piece, tuple(position))
      position[1] += 1
      put_piece(grid, random_piece, tuple(position))
    elif key == ord(' ') and can_move(grid, random_piece, tuple(position), 'r'):
      remove_piece(grid, random_piece, tuple(position))
      random_piece = rotate_piece(random_piece)
      put_piece(grid, random_piece, tuple(position))
    elif key == curses.KEY_DOWN:
      break
    # grid = clear_filled_lines(grid)
    window.clear()
    draw_grid(window, grid)
    draw_borders(window, cols, rows)
    window.refresh()
  return random_piece