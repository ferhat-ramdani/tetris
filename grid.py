
from pieces import rotate_piece


def put_piece(grid, piece, position):
  x, y = position
  piece_height = len(piece)
  piece_width = len(piece[0])

  for i in range(piece_height):
    for j in range(piece_width):
      if piece[i][j] == 'x':
        grid[x + i][y + j] = piece[i][j]

def remove_piece(grid, piece, position):
  x, y = position
  piece_height = len(piece)
  piece_width = len(piece[0])

  for i in range(piece_height):
    for j in range(piece_width):
      if piece[i][j] == 'x':
        grid[x + i][y + j] = ' '

def check_collision(grid, piece, position):
  x, y = position
  piece_height = len(piece)
  piece_width = len(piece[0])

  for i in range(piece_height):
    for j in range(piece_width):
      if piece[i][j] == 'x' and grid[x + i][y + j] == 'x':
        return True
  return False


def can_move(grid, piece, position, direction):
  x, y = position
  remove_piece(grid, piece, position)
  new_piece = piece
  
  if direction == 'l':
    new_position = (x, y - 1)
  elif direction == 'r':
    new_position = (x, y + 1)
  elif direction == 'u':
    new_position = (x - 1, y)
  elif direction == 'b':
    new_position = (x + 1, y)
  elif direction == 'r':
    new_position = position
    new_piece = rotate_piece(piece)
  else:
    raise ValueError("Invalid direction. Use 'l', 'r', 'u', 'b', or 'r'.")
  
  new_x, new_y = new_position
  piece_height = len(new_piece)
  piece_width = len(new_piece[0])
  grid_height = len(grid)
  grid_width = len(grid[0])

  if new_x < 0 or new_x + piece_height - 1 >= grid_height or new_y < 0 or new_y + piece_width - 1 >= grid_width:
    put_piece(grid, piece, position)
    return False

  collision = check_collision(grid, new_piece, new_position)
  if not collision:
    put_piece(grid, new_piece, position)
  else:
    put_piece(grid, piece, position)
  
  return not collision

def clear_filled_lines(grid):
  grid_width = len(grid[0])
  new_grid = [row for row in grid if row.count('x') != grid_width]
  lines_cleared = len(grid) - len(new_grid)
  new_grid = [[' ' for _ in range(grid_width)] for _ in range(lines_cleared)] + new_grid
  return new_grid, lines_cleared