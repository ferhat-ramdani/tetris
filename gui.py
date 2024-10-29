
import curses
import time

from grid import *

def draw_piece(window, piece, start_y, start_x):
  for y, row in enumerate(piece):
    for x, char in enumerate(row):
      if char == 'x':
        window.addch(start_y + y, start_x + x, char)

def clear_piece(window, piece, start_y, start_x):
  for y, row in enumerate(piece):
    for x, char in enumerate(row):
      if char == 'x':
        window.addch(start_y + y, start_x + x, ' ')

def draw_grid(window, grid, margin):
  for y, row in enumerate(grid):
    for x, char in enumerate(row):
      window.addch(y + 1, x + margin + 1, char)

def draw_borders(window, cols, rows, margin) :
  for x in range(cols + 2):
    window.addch(0, x + margin, '-')
    window.addch(rows + 1, x + margin, '-')
  for y in range(rows + 2):
    window.addch(y, margin, '|')
    window.addch(y, cols + 1 + margin, '|')

def handle_key_events(window, position, current_piece, next_piece, grid, margin):
  start_time = time.time()
  while time.time() - start_time < 1:
    key = window.getch()
    window.timeout(1000)
    if key == curses.KEY_LEFT and can_move(grid, current_piece, tuple(position), 'l'):
      remove_piece(grid, current_piece, tuple(position))
      position[1] -= 1
      put_piece(grid, current_piece, tuple(position))
    elif key == curses.KEY_RIGHT and can_move(grid, current_piece, tuple(position), 'r'):
      remove_piece(grid, current_piece, tuple(position))
      position[1] += 1
      put_piece(grid, current_piece, tuple(position))
    elif key == ord(' ') and can_move(grid, current_piece, tuple(position), 'rot'):
      remove_piece(grid, current_piece, tuple(position))
      current_piece = rotate_piece(current_piece)
      put_piece(grid, current_piece, tuple(position))
    elif key == curses.KEY_DOWN:
      break
    grid = clear_filled_lines(grid)[0]
    window.clear()
    update_window(window, grid, next_piece, margin)
    window.refresh()
  return current_piece

def update_window(window, grid, next_piece, margin):
  draw_grid(window, grid, margin)
  draw_borders(window, len(grid[0]), len(grid), margin)
  draw_piece(window, next_piece, len(grid[0]) // 2 - 3, 7)
  window.refresh()
