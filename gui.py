
import curses
import time

from grid import *

def draw_piece(window: curses.window, piece: List[List[str]], start_pos: tuple[int, int]):
  for y, row in enumerate(piece):
    for x, char in enumerate(row):
      if char == 'x':
        window.addch(start_pos[1] + y, start_pos[0] + x, char)

def clear_piece(window: curses.window, piece: List[List[str]], pos: tuple[int, int]):
  for y, row in enumerate(piece):
    for x, char in enumerate(row):
      if char == 'x':
        window.addch(pos[1] + y, pos[0] + x, ' ')

def draw_grid(window, matrix, margin):
  for y, row in enumerate(matrix):
    for x, char in enumerate(row):
      window.addch(y + 1, x + margin + 1, char)

def draw_borders(window: curses.window, cols: int, rows: int, margin: int) :
  for x in range(cols + 2):
    window.addch(0, x + margin, '-')
    window.addch(rows + 1, x + margin, '-')
  for y in range(rows + 2):
    window.addch(y, margin, '|')
    window.addch(y, cols + 1 + margin, '|')

def handle_key_events(window: curses.window, position: int, current_piece: List[List[str]], next_piece: List[List[str]], grid: Grid, margin: int):
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

def update_window(window: curses.window, matrix: List[List[str]], next_piece: List[List[str]], margin: int):
  draw_grid(window, matrix, margin)
  draw_borders(window, len(matrix[0]), len(matrix), margin)
  start_pos = (len(matrix[0]) // 2 - 3, 7)
  draw_piece(window, next_piece, start_pos)
  window.refresh()
