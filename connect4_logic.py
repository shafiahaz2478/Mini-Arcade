

def new_board() -> list:

    return [["." for _ in range(7)] for _ in range(6)]


def render(board: list) -> str:

    lines = ["1 2 3 4 5 6 7"]
    for row in reversed(board):
        lines.append(" ".join(row))
    return "\n".join(lines)


def column_is_full(board: list, col: int) -> bool:

    return board[5][col] != "."


def make_move(board: list, col: int, mark: str) -> list:
    for row in range(6):
        if board[row][col] == ".":
            board[row][col] = mark
            return board
    return board


def game_state(board: list) -> str:
    for mark in ("X", "O"):
        for row in range(6):
            for col in range(7):
                if board[row][col] != mark:
                    continue
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