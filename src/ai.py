"""Module containing the AI player algorithm."""
from pieces import ColoredPiece, rotate_piece

def get_best_move(grid, colored_piece: ColoredPiece) -> tuple:
    """
    Find the best move (target_rotations, target_col) for the given piece on the grid.
    Returns (best_rotations_count, best_col).
    """
    best_score = -float('inf')
    best_rotations_count = 0
    best_col = 0
    
    # Try all rotations (0 to 3)
    temp_piece = ColoredPiece(colored_piece.color_value, [row[:] for row in colored_piece.piece])
    
    for rot in range(4):
        piece_width = len(temp_piece.piece[0])
        
        # Try all columns where the piece fits
        for col_idx in range(grid.width - piece_width + 1):
            # Simulate drop
            landing_row = get_landing_row(grid, temp_piece.piece, col_idx)
            if landing_row is None:
                continue
                
            # Evaluate board state after dropping
            score = evaluate_placement(grid, temp_piece.piece, landing_row, col_idx)
            if score > best_score:
                best_score = score
                best_rotations_count = rot
                best_col = col_idx
                
        # Rotate piece for next iteration
        temp_piece.piece = rotate_piece(temp_piece.piece)
        
    return best_rotations_count, best_col

def get_landing_row(grid, piece: list, col_idx: int) -> int:
    """Find the landing row index for the piece at the given column."""
    piece_height = len(piece)
    piece_width = len(piece[0])
    
    # Check bounds
    if col_idx < 0 or col_idx + piece_width > grid.width:
        return None
        
    # Drop down row by row
    landing_row = None
    for r in range(grid.height - piece_height + 1):
        if grid.check_collision(piece, (r, col_idx)):
            break
        landing_row = r
    return landing_row

def evaluate_placement(grid, piece: list, row: int, col_idx: int) -> float:
    """Evaluate the board quality using the Pierre Dellacherie algorithm."""
    piece_height = len(piece)
    piece_width = len(piece[0])
    
    # Create simple binary representation of grid matrix
    matrix_copy = [[self_block.char != ' ' for self_block in grid_row] for grid_row in grid.matrix]
    
    # Place piece
    piece_blocks_placed = []
    for i in range(piece_height):
        for j in range(piece_width):
            if piece[i][j] == 'x':
                matrix_copy[row + i][col_idx + j] = True
                piece_blocks_placed.append((row + i, col_idx + j))
                
    # 1. Landing Height (Measured from bottom-up to center of piece)
    landing_height = grid.height - (row + piece_height / 2.0)
    
    # 2. Eroded Piece Cells
    lines_cleared = 0
    blocks_eliminated = 0
    remaining_matrix = []
    for r in range(grid.height):
        if all(matrix_copy[r]):
            lines_cleared += 1
            blocks_eliminated += sum(1 for (pr, pc) in piece_blocks_placed if pr == r)
        else:
            remaining_matrix.append(matrix_copy[r])
            
    eroded_piece_cells = lines_cleared * blocks_eliminated
    
    # Reconstruct matrix after clearing lines
    matrix_after = [[False] * grid.width for _ in range(lines_cleared)] + remaining_matrix
    
    # 3. Row Transitions
    row_transitions = 0
    for r in range(grid.height):
        if not matrix_after[r][0]:  # Left wall
            row_transitions += 1
        for c in range(grid.width - 1):
            if matrix_after[r][c] != matrix_after[r][c + 1]:
                row_transitions += 1
        if not matrix_after[r][-1]: # Right wall
            row_transitions += 1
            
    # 4. Column Transitions
    col_transitions = 0
    for c in range(grid.width):
        if matrix_after[0][c]: # Top (empty space -> block)
            col_transitions += 1
        for r in range(grid.height - 1):
            if matrix_after[r][c] != matrix_after[r + 1][c]:
                col_transitions += 1
        if not matrix_after[-1][c]: # Bottom floor
            col_transitions += 1
            
    # 5. Holes
    holes = 0
    for c in range(grid.width):
        block_found = False
        for r in range(grid.height):
            if matrix_after[r][c]:
                block_found = True
            elif block_found and not matrix_after[r][c]:
                holes += 1
                
    # 6. Well Sums
    well_sums = 0
    for c in range(grid.width):
        depth = 0
        for r in range(grid.height):
            if not matrix_after[r][c]:
                left_solid = (c == 0) or matrix_after[r][c - 1]
                right_solid = (c == grid.width - 1) or matrix_after[r][c + 1]
                if left_solid and right_solid:
                    depth += 1
                    well_sums += depth
                else:
                    depth = 0
            else:
                depth = 0
    
    # El-Tetris (Dellacherie) GA-tuned Heuristic Weights
    w_height = -4.500158
    w_eroded = 3.418126
    w_row_trans = -3.217888
    w_col_trans = -9.348695
    w_holes = -7.899265
    w_wells = -3.385597
    
    score = (w_height * landing_height) + \
            (w_eroded * eroded_piece_cells) + \
            (w_row_trans * row_transitions) + \
            (w_col_trans * col_transitions) + \
            (w_holes * holes) + \
            (w_wells * well_sums)
            
    return score
