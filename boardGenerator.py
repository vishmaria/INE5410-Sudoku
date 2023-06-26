import random

def generate_sudoku_board():
    board = [[0] * 9 for _ in range(9)]
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(9):
        random.shuffle(nums)
        board[i] = nums.copy()
    random.shuffle(board)
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

save_sudoku_boards_to_file('sudoku_boards.txt', 1000000)