"""Mini Arcade — menu launcher. All input() and print() lives here."""
import random

import battleship_logic
import blackjack_logic
import connect4_logic
import hangman_logic

MENU = """||           *Mini Arcade*           ||

1. Sudoku
2. Hangman
3. Blackjack
4. Connect 4
5. Battleship
6. Give me something
7. Exit"""


def main() -> None:
    options = {
        "1": run_sudoku,
        "2": run_hangman,
        "3": run_blackjack,
        "4": run_connect4,
        "5": run_battleship,
        "6": run_random,
    }
    while True:
        print()          # breathing room after a game
        print(MENU)
        choice = read_choice()
        if choice == "7":
            print("Thanks for playing! Goodbye.")
            return
        action = options.get(choice)
        if action is None:
            print("Invalid choice. Please enter a number between 1 and 7.")
        else:
            action()


def read_choice() -> str:
    """Menu input: thin reader. Validation is main()'s job,
    so the menu reprints on bad input."""
    return input("Enter your choice: ").strip()


def run_random() -> None:
    """Launches one of the five run functions, chosen uniformly at random."""
    functions = [run_sudoku, run_hangman, run_blackjack,
                 run_connect4, run_battleship]
    random.choice(functions)()


# ---- Hangman (Section 4.3, transcribed) -------------------------------

def read_letter(guessed: set) -> str:
    """Input is main's job: keep asking until we get a usable letter
    (or the word 'quit'). Returns a clean, valid guess."""
    while True:
        raw = input("Guess a letter (or 'quit' to quit): ").strip().lower()
        if raw == "quit":
            return raw
        if len(raw) == 1 and "a" <= raw <= "z" and raw not in guessed:
            return raw
        if raw in guessed:
            print(f"You already guessed '{raw}'.")
        else:
            print("Please enter a single letter (a-z).")


def run_hangman() -> None:
    """Hangman loop + state (word, guessed, lives)."""
    word = hangman_logic.pick_word()
    guessed, lives = set(), 6

    while True:
        print(hangman_logic.draw_gallows(lives))
        print(hangman_logic.mask_word(word, guessed))

        guess = read_letter(guessed)
        if guess == "quit":
            print(f"You quit. The word was '{word}'.")
            return

        guessed, lives, report = hangman_logic.make_move(
            word, guessed, lives, guess)
        print(report)

        status = hangman_logic.game_state(word, guessed, lives)
        if status != "in progress":
            print(status)
            return


# ---- SCAFFOLDING: replace one stub per milestone, then delete this note.

def run_sudoku() -> None:
    print("Sudoku is not built yet.")


# ---- Blackjack (Section 4.4, transcribed) -----------------------------

def read_action() -> str:
    """Blackjack input: hit / stand / quit, re-asked otherwise."""
    while True:
        raw = input("Hit or stand? (or 'quit'): ").strip().lower()
        if raw in ("h", "hit"):
            return "hit"
        if raw in ("s", "stand"):
            return "stand"
        if raw == "quit":
            return "quit"
        print("Enter hit, stand, or quit.")


def run_blackjack() -> None:
    """Blackjack loop + state (deck, player, dealer)."""
    deck = blackjack_logic.new_deck()
    deck, player, dealer = blackjack_logic.deal_initial(deck)
    print(blackjack_logic.render_hands(player, dealer, True))

    while True:
        action = read_action()
        if action == "quit":
            print("You quit the round.")
            return

        deck, player, dealer, report, status = blackjack_logic.make_move(
            deck, player, dealer, action)
        print(report)
        print(blackjack_logic.render_hands(
            player, dealer, status == "in progress"))

        if status != "in progress":
            return


# ---- Connect 4 (Section 4.5, transcribed) -----------------------------

def read_column(board: list, mark: str) -> int:
    """Connect 4 input: 1-7 and column not full, re-asked otherwise.
    Returns the 0-based column index, or the string 'quit'."""
    while True:
        raw = input(f"Player {mark}, choose a column (1-7 or 'quit'): ").strip()
        if raw == "quit":
            return raw
        if len(raw) == 1 and "1" <= raw <= "7":   # mirrors read_letter's a-z check
            col = int(raw) - 1
            if connect4_logic.column_is_full(board, col):
                print(f"Column {col + 1} is full — choose another.")
            else:
                return col
        else:
            print("Enter a column number 1-7.")


def run_connect4() -> None:
    """Connect 4 loop + state (board, whose turn)."""
    board = connect4_logic.new_board()
    mark = "X"

    while True:
        print(connect4_logic.render(board))
        col = read_column(board, mark)
        if col == "quit":
            print(f"Player {mark} quits the game.")
            return
        board = connect4_logic.make_move(board, col, mark)

        status = connect4_logic.game_state(board)
        if status != "in progress":
            print(connect4_logic.render(board))   # show the winning board...
            print(status)                         # ...then the final line
            return
        mark = "O" if mark == "X" else "X"

# ---- Battleship (Section 4.6, transcribed) ----------------------------

def read_coords(shots: set) -> tuple:
    """Battleship input: parse 'row col', cell not already fired.
    Returns the 0-based (row, col), or the string 'quit'."""
    while True:
        raw = input("Fire at row, column (or 'quit'): ").strip()
        if raw == "quit":
            return raw
        parts = raw.split()
        valid = (
            len(parts) == 2
            and all(p.isdecimal() for p in parts)
            and all(1 <= int(p) <= 10 for p in parts)
        )
        if not valid:
            print("Enter two numbers 1-10: row and column.")
            continue
        row, col = int(parts[0]) - 1, int(parts[1]) - 1
        if (row, col) in shots:
            print(f"You already fired at {row + 1} {col + 1}.")
            continue
        return (row, col)


def run_battleship() -> None:
    """Battleship loop + state (enemy_fleet, shots, player_fleet, computer_shots).
    Classic turn rule: a hit — sinking hits included — grants another shot;
    a miss passes the turn. Both sides."""
    player_fleet = battleship_logic.place_fleet()
    enemy_fleet = battleship_logic.place_fleet()
    shots, computer_shots = set(), set()

    while True:
        print(battleship_logic.render_player_board(player_fleet, computer_shots))
        print()                            # cosmetic: gap between the boards
        print(battleship_logic.render_enemy_board(enemy_fleet, shots))

        # --- your turn: keep firing while you hit ---
        while True:
            coords = read_coords(shots)
            if coords == "quit":
                print("You quit the battle.")
                return
            row, col = coords
            shots, outcome, report = battleship_logic.make_move(
                enemy_fleet, shots, row, col)
            print(report)
            print(battleship_logic.render_enemy_board(enemy_fleet, shots))
            status = battleship_logic.game_state(
                enemy_fleet, shots, player_fleet, computer_shots)
            if status != "in progress":
                print(status)
                return
            if outcome == "miss":
                break                       # your turn ends — pass it over

        while True:
            computer_shots, outcome, report = battleship_logic.computer_fire(
                player_fleet, computer_shots)
            print(report)
            print(battleship_logic.render_player_board(
                player_fleet, computer_shots))
            status = battleship_logic.game_state(
                enemy_fleet, shots, player_fleet, computer_shots)
            if status != "in progress":
                print(status)
                return
            if outcome == "miss":
                break

if __name__ == "__main__":
    main()