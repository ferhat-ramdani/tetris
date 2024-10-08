
class Grid:
  def __init__(self, rows, cols, default_value=0):
    self.rows = rows
    self.cols = cols
    self.grid = [[default_value for _ in range(cols)] for _ in range(rows)]

  def set(self, row: int, col: int):
    return self.grid[row][col]

  def clear(self, row: int, col: int):
    self.grid[row][col] = ' '

  def display(self):
    for row in self.grid:
      print(f"*{row}*")