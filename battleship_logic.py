
import random

GRID_SIZE = 10
SHIPS = [
    ("Carrier", 5),
    ("Battleship", 4),
    ("Submarine", 3),
    ("Cruiser", 3),
    ("Destroyer", 2),
]


def place_fleet() -> list:
    fleet = []
    placed_cells = set()
    for name, length in SHIPS:
        while True:
            horizontal = random.choice((True, False))
            if horizontal:
                row = random.randrange(GRID_SIZE)
                col = random.randrange(GRID_SIZE - length + 1)
                cells = {(row, col + i) for i in range(length)}
            else:
                row = random.randrange(GRID_SIZE - length + 1)
                col = random.randrange(GRID_SIZE)
                cells = {(row + i, col) for i in range(length)}
            if not cells & placed_cells:
                break
        fleet.append((name, cells))
        placed_cells |= cells
    return fleet


def is_sunk(cells: set, shots: set) -> bool:
    return cells <= shots


def make_move(fleet: list, shots: set, row: int, col: int) -> tuple:

    shots.add((row, col))
    for name, cells in fleet:
        if (row, col) in cells:
            if is_sunk(cells, shots):
                return shots, "hit", f"Hit — you sank the enemy {name}!"
            return shots, "hit", "Hit!"
    return shots, "miss", "Miss."


def computer_fire(player_fleet: list, computer_shots: set) -> tuple:

    row, col = random.randrange(GRID_SIZE), random.randrange(GRID_SIZE)
    while (row, col) in computer_shots:
        row, col = random.randrange(GRID_SIZE), random.randrange(GRID_SIZE)
    computer_shots.add((row, col))
    for name, cells in player_fleet:
        if (row, col) in cells:
            if is_sunk(cells, computer_shots):
                report = f"The computer fires at {row + 1} {col + 1} — it sinks your {name}!"
            else:
                report = f"The computer fires at {row + 1} {col + 1} — a hit!"
            return computer_shots, "hit", report
    return computer_shots, "miss", f"The computer fires at {row + 1} {col + 1} — a miss."

def render_player_board(fleet: list, computer_shots: set) -> str:
    ship_cells = set()
    for name, cells in fleet:
        ship_cells |= cells
    lines = ["    " + " ".join(str(c + 1) for c in range(GRID_SIZE))]
    for row in range(GRID_SIZE):
        row_cells = []
        for col in range(GRID_SIZE):
            cell = (row, col)
            if cell in computer_shots and cell in ship_cells:
                row_cells.append("X")
            elif cell in computer_shots:
                row_cells.append("o")
            elif cell in ship_cells:
                row_cells.append("#")
            else:
                row_cells.append(".")
        body = " ".join(row_cells[:-1]) + "  " + row_cells[-1]
        lines.append(f"{row + 1:>2}  {body}")
    return "\n".join(lines)


def render_enemy_board(fleet: list, shots: set) -> str:
    lines = ["    " + " ".join(str(c + 1) for c in range(GRID_SIZE))]
    for row in range(GRID_SIZE):
        row_cells = []
        for col in range(GRID_SIZE):
            cell = (row, col)
            if cell not in shots:
                row_cells.append(".")
                continue
            symbol = "o"
            for name, cells in fleet:
                if cell in cells:
                    symbol = "*" if is_sunk(cells, shots) else "X"
            row_cells.append(symbol)
        body = " ".join(row_cells[:-1]) + "  " + row_cells[-1]
        lines.append(f"{row + 1:>2}  {body}")
    return "\n".join(lines)


def game_state(enemy_fleet: list, shots: set, player_fleet: list,
               computer_shots: set) -> str:
    if all(is_sunk(cells, shots) for name, cells in enemy_fleet):
        return "You win — the enemy fleet is destroyed!"
    if all(is_sunk(cells, computer_shots) for name, cells in player_fleet):
        return "You lose — your fleet is destroyed!"
    return "in progress"