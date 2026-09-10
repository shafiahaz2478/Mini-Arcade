"""battleship_logic.py — pure functions: no input(), no print().

Every function is Section 4.6 of the design doc, transcribed.
read_coords in main.py guarantees shots are in range and not
already fired, so make_move never re-validates.

A ship is a (name, cells) tuple, cells being a set of 0-based
(row, col) pairs; a fleet is a list of five ships. Shots are
sets of (row, col) cells. Coordinates convert to 1-based only
at the display edges.
"""
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
    """Random legal placement of the 5 ships. Called twice, once per side."""
    fleet = []
    placed_cells = set()
    for name, length in SHIPS:
        while True:                        # retry until the ship fits
            horizontal = random.choice((True, False))
            if horizontal:
                row = random.randrange(GRID_SIZE)
                col = random.randrange(GRID_SIZE - length + 1)
                cells = {(row, col + i) for i in range(length)}
            else:
                row = random.randrange(GRID_SIZE - length + 1)
                col = random.randrange(GRID_SIZE)
                cells = {(row + i, col) for i in range(length)}
            if not cells & placed_cells:   # no overlap — touching is fine
                break
        fleet.append((name, cells))
        placed_cells |= cells
    return fleet


def is_sunk(cells: set, shots: set) -> bool:
    """True when every cell of the ship has been hit."""
    return cells <= shots                  # subset: all cells fired at


def make_move(fleet: list, shots: set, row: int, col: int) -> tuple:
    """You fire: (shots, report) — hit / miss / sank a named ship."""
    shots.add((row, col))
    for name, cells in fleet:
        if (row, col) in cells:
            if is_sunk(cells, shots):
                return shots, f"Hit — you sank the enemy {name}!"
            return shots, "Hit!"
    return shots, "Miss."


def computer_fire(player_fleet: list, computer_shots: set) -> tuple:
    """The computer opponent: picks an unfired cell, fires.
    Returns (computer_shots, report)."""
    row, col = random.randrange(GRID_SIZE), random.randrange(GRID_SIZE)
    while (row, col) in computer_shots:    # rejection: uniform over unfired cells
        row, col = random.randrange(GRID_SIZE), random.randrange(GRID_SIZE)
    computer_shots.add((row, col))
    for name, cells in player_fleet:
        if (row, col) in cells:
            if is_sunk(cells, computer_shots):
                report = f"The computer fires at {row + 1} {col + 1} — it sinks your {name}!"
            else:
                report = f"The computer fires at {row + 1} {col + 1} — a hit!"
            return computer_shots, report
    return computer_shots, f"The computer fires at {row + 1} {col + 1} — a miss."


def render_player_board(fleet: list, computer_shots: set) -> str:
    """Your waters: ships visible, computer's hits and misses."""
    ship_cells = set()
    for name, cells in fleet:
        ship_cells |= cells
    lines = ["    " + " ".join(str(c + 1) for c in range(GRID_SIZE))]
    for row in range(GRID_SIZE):
        row_cells = []
        for col in range(GRID_SIZE):
            cell = (row, col)
            if cell in computer_shots and cell in ship_cells:
                row_cells.append("X")      # hit on you — overrides # (order matters)
            elif cell in computer_shots:
                row_cells.append("o")      # miss on you
            elif cell in ship_cells:
                row_cells.append("#")      # intact ship
            else:
                row_cells.append(".")      # water
        body = " ".join(row_cells[:-1]) + "  " + row_cells[-1]  # col 10 under the '10'
        lines.append(f"{row + 1:>2}  {body}")
    return "\n".join(lines)


def render_enemy_board(fleet: list, shots: set) -> str:
    """Target grid: your hits and misses; ships hidden."""
    lines = ["    " + " ".join(str(c + 1) for c in range(GRID_SIZE))]
    for row in range(GRID_SIZE):
        row_cells = []
        for col in range(GRID_SIZE):
            cell = (row, col)
            if cell not in shots:
                row_cells.append(".")      # unknown waters
                continue
            symbol = "o"                   # fired here — miss by default
            for name, cells in fleet:
                if cell in cells:
                    symbol = "*" if is_sunk(cells, shots) else "X"
            row_cells.append(symbol)
        body = " ".join(row_cells[:-1]) + "  " + row_cells[-1]
        lines.append(f"{row + 1:>2}  {body}")
    return "\n".join(lines)


def game_state(enemy_fleet: list, shots: set, player_fleet: list,
               computer_shots: set) -> str:
    """'in progress' / you win / you lose — checked after each fire, both ways."""
    if all(is_sunk(cells, shots) for name, cells in enemy_fleet):
        return "You win — the enemy fleet is destroyed!"
    if all(is_sunk(cells, computer_shots) for name, cells in player_fleet):
        return "You lose — your fleet is destroyed!"
    return "in progress"