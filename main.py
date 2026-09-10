
import random

import battleship_logic
import blackjack_logic
import connect4_logic
import hangman_logic
import sudoku_logic

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
        print()
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
    return input("Enter your choice: ").strip()


def run_random() -> None:
    functions = [run_sudoku, run_hangman, run_blackjack,
                 run_connect4, run_battleship]
    random.choice(functions)()



def read_letter(guessed: set) -> str:
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



def read_move(board: list, givens: set) -> tuple:
    while True:
        raw = input("Row, column, value (0 erases, or 'quit'): ").strip()
        if raw == "quit":
            return raw
        parts = raw.split()
        valid = (
            len(parts) == 3
            and all(p.isdecimal() for p in parts)
            and 1 <= int(parts[0]) <= 9
            and 1 <= int(parts[1]) <= 9
            and 0 <= int(parts[2]) <= 9
        )
        if not valid:
            print("Enter three numbers: row 1-9, column 1-9, value 0-9.")
            continue
        row, col, value = int(parts[0]) - 1, int(parts[1]) - 1, int(parts[2])
        if (row, col) in givens:
            print("That cell is part of the puzzle — it can't be changed.")
            continue
        if value == 0:
            return (row, col, 0)
        if not sudoku_logic.is_valid_placement(board, row, col, value):
            print(f"{value} doesn't fit there — its row, column, or box "
                  f"already has a {value}.")
            continue
        return (row, col, value)


def run_sudoku() -> None:
    board, givens = sudoku_logic.new_puzzle()

    while True:
        print(sudoku_logic.render_board(board, givens))
        move = read_move(board, givens)
        if move == "quit":
            print("You quit this puzzle.")
            return
        row, col, value = move
        board = sudoku_logic.make_move(board, row, col, value)

        status = sudoku_logic.game_state(board)
        if status != "in progress":
            print(sudoku_logic.render_board(board, givens))   # final board...
            print(status)                                     # ...then the line
            return



def read_action() -> str:
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


def read_column(board: list, mark: str) -> int:
    while True:
        raw = input(f"Player {mark}, choose a column (1-7 or 'quit'): ").strip()
        if raw == "quit":
            return raw
        if len(raw) == 1 and "1" <= raw <= "7":
            col = int(raw) - 1
            if connect4_logic.column_is_full(board, col):
                print(f"Column {col + 1} is full — choose another.")
            else:
                return col
        else:
            print("Enter a column number 1-7.")


def run_connect4() -> None:
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
            print(connect4_logic.render(board))
            print(status)
            return
        mark = "O" if mark == "X" else "X"

def read_coords(shots: set) -> tuple:
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
    player_fleet = battleship_logic.place_fleet()
    enemy_fleet = battleship_logic.place_fleet()
    shots, computer_shots = set(), set()

    while True:
        print(battleship_logic.render_player_board(player_fleet, computer_shots))
        print()
        print(battleship_logic.render_enemy_board(enemy_fleet, shots))

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
                break

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