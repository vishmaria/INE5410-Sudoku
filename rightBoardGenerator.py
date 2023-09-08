import random

def is_valid(board, row, col, num):
    # Check if the number already exists in the current row
    for i in range(9):
        if board[row][i] == num:
            return False

    # Check if the number already exists in the current column
    for i in range(9):
        if board[i][col] == num:
            return False

    # Check if the number already exists in the current 3x3 grid
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                # Try each number from 1 to 9
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num

                        if solve_sudoku(board):
                            return True

                        board[row][col] = 0  # Backtrack

                return False  # No valid number found

    return True  # All cells filled, solution found

def generate_sudoku_board():
    board = [[0] * 9 for _ in range(9)]
    solve_sudoku(board)
    return board

def save_sudoku_boards_to_file(file_path, num_boards):
    with open(file_path, 'w') as file:
        for _ in range(num_boards):
            board = generate_sudoku_board()
            for i in range(9):
                for j in range(9):
                    file.write(str(board[i][j]))
                file.write('\n')
            if _ != num_boards - 1:
                file.write('\n')

save_sudoku_boards_to_file('sudoku_boards.txt', 100000)
print('done')