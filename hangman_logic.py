"""hangman_logic.py — pure functions: no input(), no print().

Every function is Section 4.3 of the design doc, transcribed.
read_letter in main.py guarantees guesses are valid and new,
so nothing here re-validates.
"""
import random

WORDLIST = [
    "python", "arcade", "terminal", "keyboard", "function",
    "variable", "loop", "module", "debug", "compile",
]

# One drawing per wrong guess, 0 to 6 (GALLOWS[6 - lives]).
GALLOWS = [
    "  +---+\n  |   |\n      |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n  |   |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|   |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n=========",
    "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n=========",
]


def pick_word() -> str:
    """Random secret word from WORDLIST. The only random function."""
    return random.choice(WORDLIST)


def draw_gallows(lives: int) -> str:
    """Gallows for the current lives (6 = empty, 0 = complete)."""
    return GALLOWS[6 - lives]


def mask_word(word: str, guessed: set) -> str:
    """The 'h _ n _ m _ n' line."""
    return " ".join(ch if ch in guessed else "_" for ch in word)


def make_move(word: str, guessed: set, lives: int, guess: str) -> tuple:
    """All hangman rules live here. Takes a valid, never-guessed letter.
    Returns (guessed, lives, report)."""
    guessed.add(guess)
    if guess in word:
        return guessed, lives, f"Yes! '{guess}' is in the word."
    return guessed, lives - 1, f"Nope, '{guess}' is not in the word."


def game_state(word: str, guessed: set, lives: int) -> str:
    """'in progress', or the final line main.py prints."""
    if all(ch in guessed for ch in word):
        return f"You won! The word was '{word}'."
    if lives == 0:
        return f"You lost! The word was '{word}'."
    return "in progress"