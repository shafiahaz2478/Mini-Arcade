
import random

CELLS_TO_REMOVE = 48


BASE_SOLUTION = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9],
]


def random_solution() -> list:
    grid = [row[:] for row in BASE_SOLUTION]

    labels = list(range(1, 10))
    random.shuffle(labels)
    grid = [[labels[cell - 1] for cell in row] for row in grid]
    def shuffle_rows(grid):
        bands = [grid[0:3], grid[3:6], grid[6:9]]
        for band in bands:
            random.shuffle(band)
        random.shuffle(bands)
        return [row for band in bands for row in band]

    grid = shuffle_rows(grid)

    grid = [list(col) for col in zip(*grid)]
    grid = shuffle_rows(grid)
    grid = [list(col) for col in zip(*grid)]

    return grid


def new_puzzle() -> tuple:
    board = random_solution()
    cells = [(row, col) for row in range(9) for col in range(9)]
    for row, col in random.sample(cells, CELLS_TO_REMOVE):
        board[row][col] = 0
    givens = {(row, col) for row in range(9) for col in range(9)
              if board[row][col] != 0}
    return board, givens


def render_board(board: list, givens: set) -> str:
    labels = [f" {n} " for n in range(1, 10)]
    lines = ["   " + "".join(labels[0:3]) + "|" + "".join(labels[3:6])
             + "|" + "".join(labels[6:9])]
    for row in range(9):
        fields = []
        for col in range(9):
            value = board[row][col]
            if value == 0:
                fields.append(" . ")           # empty
            elif (row, col) in givens:
                fields.append(f" {value} ")    # given
            else:
                fields.append(f"[{value}]")    # player entry
        lines.append(f"{row + 1:>2} " + "".join(fields[0:3]) + "|"
                     + "".join(fields[3:6]) + "|" + "".join(fields[6:9]))
        if row in (2, 5):
            lines.append("   " + "-" * 9 + "+" + "-" * 9 + "+" + "-" * 9) # + separator
    return "\n".join(lines)


def is_valid_placement(board: list, row: int, col: int, value: int) -> bool:
    for c in range(9):
        if c != col and board[row][c] == value:
            return False
    for r in range(9):
        if r != row and board[r][col] == value:
            return False
    box_row, box_col = row - (row % 3), col - (col % 3)
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if (r, c) != (row, col) and board[r][c] == value:
                return False
    return True


def make_move(board: list, row: int, col: int, value: int) -> list:
    board[row][col] = value
    return board


def game_state(board: list) -> str:
    if all(0 not in row for row in board):
        return "Solved! Well played."
    return "in progress"