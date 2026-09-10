"""blackjack_logic.py — pure functions: no input(), no print().

Every function is Section 4.4 of the design doc, transcribed.
read_action in main.py guarantees actions are hit/stand/quit,
so make_move only ever sees "hit" or "stand".

A card is a (rank, suit) tuple, e.g. ("A", "S"). The deck is a
list; the top of the deck is the last element (every draw is pop()).
"""
import random

SUITS = ["S", "H", "D", "C"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


def new_deck() -> list:
    """Fresh shuffled 52-card deck. One per round."""
    deck = [(rank, suit) for suit in SUITS for rank in RANKS]
    random.shuffle(deck)
    return deck


def deal_initial(deck: list) -> tuple:
    """(deck, player, dealer) with two cards each.
    The dealer's SECOND card is the hole card."""
    player = [deck.pop(), deck.pop()]
    dealer = [deck.pop(), deck.pop()]
    return deck, player, dealer


def hand_value(cards: list) -> int:
    """Best total with aces as 1 or 11."""
    total, aces = 0, 0
    for rank, suit in cards:
        if rank in ("J", "Q", "K"):
            total += 10
        elif rank == "A":
            total += 11
            aces += 1
        else:
            total += int(rank)
    while total > 21 and aces > 0:
        total -= 10          # recount an ace as 1
        aces -= 1
    return total


def render_hands(player: list, dealer: list, hide_dealer_card: bool) -> str:
    """Both hands with values; hole card hidden while the player
    is still playing."""
    if hide_dealer_card:
        up_rank, up_suit = dealer[0]
        dealer_cards = up_rank + up_suit + " XX"
        dealer_total = hand_value([dealer[0]])       # up card alone
    else:
        dealer_cards = " ".join(rank + suit for rank, suit in dealer)
        dealer_total = hand_value(dealer)
    dealer_line = f"Dealer: {dealer_cards} ({dealer_total})"

    player_cards = " ".join(rank + suit for rank, suit in player)
    player_line = f"You:    {player_cards} ({hand_value(player)})"

    return dealer_line + "\n" + player_line


def dealer_turn(deck: list, dealer: list) -> tuple:
    """The computer opponent: draws to 17. Returns (deck, dealer, summary)."""
    while hand_value(dealer) < 17:
        dealer.append(deck.pop())
    total = hand_value(dealer)
    if total > 21:
        summary = f"Dealer busts with {total}"
    else:
        summary = f"Dealer stands on {total}"
    return deck, dealer, summary


def make_move(deck: list, player: list, dealer: list, action: str) -> tuple:
    """Hit draws and checks bust; stand settles the round via dealer_turn.
    Returns (deck, player, dealer, report, status)."""
    if action == "hit":
        card = deck.pop()
        player.append(card)
        name, total = card[0] + card[1], hand_value(player)
        if total > 21:
            report = f"You draw the {name} — bust with {total}. You lose this round."
            return deck, player, dealer, report, "lost"
        return deck, player, dealer, f"You draw the {name}.", "in progress"

    # action == "stand"
    deck, dealer, summary = dealer_turn(deck, dealer)
    you, them = hand_value(player), hand_value(dealer)
    if them > 21:
        report, status = summary + " — you win!", "won"
    elif you > them:
        report, status = summary + f", you have {you} — you win!", "won"
    elif you < them:
        report, status = summary + f", you have {you} — you lose.", "lost"
    else:
        report, status = summary + f", you have {you} — push.", "push"
    return deck, player, dealer, report, status