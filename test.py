import random

from pieces import *
from gui import *
from grid import *

COLS = 30
ROWS = 40

start_pos = (1, COLS // 2 - 1)


def main():
  pieces = read_pieces('pieces')
  grid = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
  random_piece = random.choice(pieces)
  put_piece(random_piece, grid, start_pos)
  print(grid)

main()