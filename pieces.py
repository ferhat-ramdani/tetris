import os

def read_pieces(pieces_folder):
  pieces = []

  for piece_name in os.listdir(pieces_folder):
    path = os.path.join(pieces_folder, piece_name)
    if os.path.isfile(path):
      with open(path, 'r') as file:
        piece = [list(line.replace('\n', '')) for line in file]
        pieces.append(piece)

  return pieces

def rotate_piece(piece):
  return [list(row) for row in zip(*reversed(piece))]
