"""connect4_logic.py — pure functions: no input(), no print().

Every function is Section 4.5 of the design doc, transcribed.
read_column in main.py guarantees columns are in range and not
full, so make_move never re-validates.

Board convention: 6 rows x 7 columns. Row 0 is the BOTTOM row —
render, make_move, column_is_full and game_state all rely on it.
"""


def new_board() -> list:
    """Empty 6x7 board. Every cell is '.'."""
    return [["." for _ in range(7)] for _ in range(6)]


def render(board: list) -> str:
    """The grid with column numbers 1-7, top row printed first."""
    lines = ["1 2 3 4 5 6 7"]
    for row in reversed(board):          # bottom row is stored first
        lines.append(" ".join(row))
    return "\n".join(lines)


def column_is_full(board: list, col: int) -> bool:
    """Called by main's read_column."""
    return board[5][col] != "."          # row 5 is the top of the board


def make_move(board: list, col: int, mark: str) -> list:
    """Drops the disc with gravity, returns the board."""
    for row in range(6):                 # scan from the bottom row upward
        if board[row][col] == ".":
            board[row][col] = mark
            return board
    return board                         # unreachable: read_column guarantees a space


def game_state(board: list) -> str:
    """Checks both marks: 'in progress' / X wins / O wins / draw."""
    for mark in ("X", "O"):
        for row in range(6):
            for col in range(7):
                if board[row][col] != mark:
                    continue
                # Right, down, down-right, down-left. Row 0 is the bottom,
                # so 'down' on screen means row - 1. Checking these four
                # directions from every cell covers every possible line.
                for step_row, step_col in ((0, 1), (-1, 0), (-1, 1), (-1, -1)):
                    if all(
                        0 <= row + step_row * i < 6
                        and 0 <= col + step_col * i < 7
                        and board[row + step_row * i][col + step_col * i] == mark
                        for i in (1, 2, 3)
                    ):
                        return f"Player {mark} wins!"
    if all(cell != "." for row in board for cell in row):
        return "The board is full — a draw."
    return "in progress"