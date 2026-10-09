# Mini Arcade

**Team 16**

| Name | USN |
|------|-----|
| Aiman Patil | AU25UG075 |
| Mohammed Shafi | AU25UG036 |

A terminal-based games app written in Python. One menu gives access to five classic games, a random-pick option, and a clean exit. Each game runs until it ends (win, loss, or quit) and then returns you to the menu.

## Games

| # | Game | Mode |
|---|------|------|
| 1 | Sudoku | Solo puzzle |
| 2 | Hangman | Solo word guessing |
| 3 | Blackjack | You vs the dealer |
| 4 | Connect 4 | Two players, same keyboard |
| 5 | Battleship | You vs the computer |
| 6 | Give me something | Launches one of the five at random |
| 7 | Exit | Closes the app |

## Requirements

- Python 3.6 or newer
- No third-party packages

## How to run

```
python main.py
```

You will see:

```
||           *Mini Arcade*           ||

1. Sudoku
2. Hangman
3. Blackjack
4. Connect 4
5. Battleship
6. Give me something
7. Exit
Enter your choice:
```

Type a number from 1 to 7 and press Enter. Anything else prints an error and shows the menu again.

Typing `quit` (any capitalisation) at any game prompt ends that game and returns you to the menu.

## How each game works

### Sudoku
- A fresh random puzzle every time: 33 cells are given, 48 are empty.
- Enter a move as `row column value`, for example `3 5 7` (all numbers 1-9).
- Given cells are shown plain, your entries are shown in `[brackets]`, empty cells as `.`.
- A move that repeats a number in its row, column, or 3x3 box is rejected.
- Enter `0` as the value (for example `3 5 0`) to erase one of your own entries. Given cells cannot be changed.
- You win when every cell is filled.

### Hangman
- The computer picks a secret word from a built-in list.
- Guess one letter at a time. You have 6 wrong guesses before the figure is complete.
- Repeated guesses and invalid input cost nothing.
- Quitting reveals the word.

### Blackjack
- Type `hit` (or `h`) to draw a card, `stand` (or `s`) to stop.
- The dealer's second card stays hidden (`XX`) until the round ends.
- Face cards count 10, an Ace counts 11 or 1, whichever is better for the hand.
- If you bust, you lose immediately and the dealer does not play.
- If you stand, the dealer draws until reaching 17 or more and stands on every 17. Higher total wins, equal totals are a push.
- No betting, splitting, or doubling down. One round per session.

### Connect 4
- Two players take turns on the same keyboard. X goes first.
- Type a column number from 1 to 7 to drop a disc.
- Four in a row (horizontal, vertical, or diagonal) wins. A full board with no line is a draw.

### Battleship
- 10 x 10 grid. Each side has five ships: Carrier (5), Battleship (4), Submarine (3), Cruiser (3), Destroyer (2), placed randomly.
- Fire by typing `row column`, for example `3 4`.
- Your waters show your ships (`#`), hits on you (`X`), and misses (`o`).
- The enemy grid shows your hits (`X`), misses (`o`), and sunk ships (`*`).
- A hit lets you fire again. Your turn ends when you miss, then the computer fires the same way.
- The computer fires at random unfired cells.
- First side to sink the other's whole fleet wins.

## Project structure

```
main.py              Menu, all input() and print(), and every game loop
sudoku_logic.py      Sudoku rules (no input or printing)
hangman_logic.py     Hangman rules
blackjack_logic.py   Blackjack rules
connect4_logic.py    Connect 4 rules
battleship_logic.py  Battleship rules
tests/               Automated tests
```

### Design idea

All typing and printing lives in `main.py`. The five `*_logic.py` files hold only game rules: they take the current state in and return the new state out, and remember nothing between calls. This keeps the rules easy to test without simulating a keyboard.

## Running the tests

Install pytest (if not already installed):

```
pip install pytest
```

Run the full suite from the project root:

```
pytest
```

To run one game's tests:

```
pytest tests/test_blackjack.py
```

To see verbose output with each test name:

```
pytest -v
```

| File | What it covers |
|------|----------------|
| `tests/test_sudoku.py` | Sudoku logic, input, and full sessions |
| `tests/test_hangman.py` | Hangman logic, input, and full sessions |
| `tests/test_blackjack.py` | Blackjack logic, input, and full sessions |
| `tests/test_connect4.py` | Connect 4 logic, input, and full sessions |
| `tests/test_battleship.py` | Battleship logic, input, and full sessions |
| `tests/helpers.py` | Shared helper that fakes typed input (not a test file) |

There are 157 tests in total.
