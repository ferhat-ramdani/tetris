
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

def draw_grid(window, matrix, margin):
  for y, row in enumerate(matrix):
    for x, char in enumerate(row):
      window.addch(y + 1, x + margin + 1, char)

def draw_borders(window, cols, rows, margin) :
  for x in range(cols + 2):
    window.addch(0, x + margin, '-')
    window.addch(rows + 1, x + margin, '-')
  for y in range(rows + 2):
    window.addch(y, margin, '|')
    window.addch(y, cols + 1 + margin, '|')

def handle_key_events(window, position, current_piece, next_piece, grid: Grid, margin):
  start_time = time.time()
  while time.time() - start_time < 1:
    key = window.getch()
    window.timeout(1000)
    if key == curses.KEY_LEFT and grid.can_move(current_piece, tuple(position), 'l'):
      grid.remove_piece(current_piece, tuple(position))
      position[1] -= 1
      grid.put_piece(current_piece, tuple(position))
    elif key == curses.KEY_RIGHT and grid.can_move(current_piece, tuple(position), 'r'):
      grid.remove_piece(current_piece, tuple(position))
      position[1] += 1
      grid.put_piece(current_piece, tuple(position))
    elif key == ord(' ') and grid.can_move(current_piece, tuple(position), 'rot'):
      grid.remove_piece(current_piece, tuple(position))
      current_piece = rotate_piece(current_piece)
      grid.put_piece(current_piece, tuple(position))
    elif key == curses.KEY_DOWN:
      break
    grid.matrix = grid.clear_filled_lines()[0]
    window.clear()
    update_window(window, grid.matrix, next_piece, margin)
    window.refresh()
  return current_piece

def update_window(window, matrix, next_piece, margin):
  draw_grid(window, matrix, margin)
  draw_borders(window, len(matrix[0]), len(matrix), margin)
  draw_piece(window, next_piece, len(matrix[0]) // 2 - 3, 7)
  window.refresh()
