
import random

WORDLIST = [
    "python", "arcade", "terminal", "keyboard", "function",
    "variable", "loop", "module", "debug", "compile",
]


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
    return random.choice(WORDLIST)


def draw_gallows(lives: int) -> str:
    return GALLOWS[6 - lives]


def mask_word(word: str, guessed: set) -> str:
    return " ".join(ch if ch in guessed else "_" for ch in word)


def make_move(word: str, guessed: set, lives: int, guess: str) -> tuple:
    guessed.add(guess)
    if guess in word:
        return guessed, lives, f"Yes! '{guess}' is in the word."
    return guessed, lives - 1, f"Nope, '{guess}' is not in the word."


def game_state(word: str, guessed: set, lives: int) -> str:
    if all(ch in guessed for ch in word):
        return f"You won! The word was '{word}'."
    if lives == 0:
        return f"You lost! The word was '{word}'."
    return "in progress"