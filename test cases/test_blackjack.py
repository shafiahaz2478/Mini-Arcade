import unittest
from unittest import mock

import blackjack_logic as bj
import main
from helpers import play, ordered

class TestBlackjackLogic(unittest.TestCase):
    def test_deck(self):
        d = bj.new_deck()
        self.assertEqual(len(d), 52)
        self.assertEqual(len(set(d)), 52)

    def test_deck_is_shuffled(self):
        self.assertNotEqual(bj.new_deck(), bj.new_deck())

    def test_deal_initial(self):
        d = bj.new_deck()
        d2, p, dl = bj.deal_initial(d)
        self.assertEqual((len(p), len(dl), len(d2)), (2, 2, 48))
        self.assertEqual(len(set(p + dl)), 4)

    def test_hand_values(self):
        cases = [
            ([("K", "S"), ("Q", "H")], 20),
            ([("A", "S"), ("K", "H")], 21),
            ([("A", "S"), ("A", "H")], 12),
            ([("A", "S"), ("A", "H"), ("9", "D")], 21),
            ([("A", "S"), ("6", "H")], 17),
            ([("A", "S"), ("6", "H"), ("10", "D")], 17),
            ([("10", "S"), ("5", "H"), ("8", "D")], 23),
            ([("2", "S")], 2),
            ([("J", "S")], 10),
            ([("A", "S"), ("A", "H"), ("A", "D"), ("A", "C")], 14),
            ([("10", "S"), ("10", "H"), ("A", "D")], 21),
        ]
        for cards, want in cases:
            self.assertEqual(bj.hand_value(cards), want, cards)

    def test_render_hidden_hole_card(self):
        out = bj.render_hands([("10", "H"), ("9", "S")], [("A", "S"), ("K", "D")], True)
        self.assertEqual(out.split("\n")[0], "Dealer: AS XX (11)")
        self.assertEqual(out.split("\n")[1], "You:    10H 9S (19)")

    def test_render_revealed(self):
        out = bj.render_hands([("10", "H"), ("9", "S")], [("A", "S"), ("K", "D")], False)
        self.assertEqual(out.split("\n")[0], "Dealer: AS KD (21)")

    def test_hit_safe(self):
        d, p, dl, rep, st = bj.make_move([("2", "S")], [("10", "H"), ("5", "S")],
                                         [("2", "S"), ("2", "H")], "hit")
        self.assertEqual((rep, st), ("You draw the 2S.", "in progress"))

    def test_hit_to_exactly_21_does_not_auto_stand(self):
        d, p, dl, rep, st = bj.make_move([("6", "S")], [("10", "H"), ("5", "S")],
                                         [("2", "S"), ("2", "H")], "hit")
        self.assertEqual(st, "in progress")

    def test_hit_bust_dealer_untouched(self):
        dealer = [("2", "S"), ("2", "H")]
        d, p, dl, rep, st = bj.make_move([("5", "S")], [("10", "H"), ("9", "S")],
                                         dealer, "hit")
        self.assertEqual(rep, "You draw the 5S — bust with 24. You lose this round.")
        self.assertEqual(st, "lost")
        self.assertEqual(len(dl), 2)

    def stand(self, player, dealer, deck):
        return bj.make_move(deck, player, dealer, "stand")

    def test_stand_dealer_busts(self):
        r = self.stand([("10", "H"), ("9", "S")], [("10", "S"), ("6", "H")], [("10", "C")])
        self.assertEqual((r[3], r[4]), ("Dealer busts with 26 — you win!", "won"))

    def test_stand_player_wins(self):
        r = self.stand([("10", "H"), ("Q", "S")], [("10", "S"), ("6", "H")], [("3", "C")])
        self.assertEqual((r[3], r[4]),
                         ("Dealer stands on 19, you have 20 — you win!", "won"))

    def test_stand_player_loses(self):
        r = self.stand([("10", "H"), ("7", "S")], [("10", "S"), ("6", "H")], [("3", "C")])
        self.assertEqual((r[3], r[4]),
                         ("Dealer stands on 19, you have 17 — you lose.", "lost"))

    def test_stand_push(self):
        r = self.stand([("10", "H"), ("9", "S")], [("10", "S"), ("6", "H")], [("3", "C")])
        self.assertEqual((r[3], r[4]),
                         ("Dealer stands on 19, you have 19 — push.", "push"))

    def test_dealer_stands_on_hard_17(self):
        r = self.stand([("10", "H"), ("9", "S")], [("10", "S"), ("7", "H")], [("2", "C")])
        self.assertEqual(len(r[2]), 2)

    def test_dealer_stands_on_soft_17(self):
        r = self.stand([("10", "H"), ("9", "S")], [("A", "S"), ("6", "H")], [("2", "C")])
        self.assertEqual(len(r[2]), 2)
        self.assertIn("Dealer stands on 17", r[3])

    def test_dealer_hits_on_16(self):
        r = self.stand([("10", "H"), ("9", "S")], [("10", "S"), ("6", "H")], [("2", "C")])
        self.assertEqual(len(r[2]), 3)

    def test_dealer_draws_multiple_cards(self):
        r = self.stand([("10", "H"), ("9", "S")], [("2", "S"), ("2", "C")],
                       ordered([("5", "D"), ("4", "D"), ("6", "D")]))
        self.assertGreaterEqual(bj.hand_value(r[2]), 17)
        self.assertGreater(len(r[2]), 3)

    def test_dealer_21_beats_player_20(self):
        r = self.stand([("10", "H"), ("K", "S")], [("A", "S"), ("K", "H")], [("2", "C")])
        self.assertEqual(r[4], "lost")


class TestBlackjackInput(unittest.TestCase):
    def test_accepted_words(self):
        for raw, want in [("h", "hit"), ("HIT", "hit"), (" Hit ", "hit"),
                          ("s", "stand"), ("Stand", "stand"), ("quit", "quit"),
                          ("QUIT", "quit")]:
            r, _ = play(main.read_action, [raw])
            self.assertEqual(r, want)

    def test_invalid_reasked(self):
        for bad in ["", "x", "hitt", "1", "hit me"]:
            r, out = play(main.read_action, [bad, "s"])
            self.assertEqual(r, "stand")
            self.assertIn("Enter hit, stand, or quit.", out)

    def test_prompt(self):
        _, out = play(main.read_action, ["s"])
        self.assertIn("Hit or stand? (or 'quit'): ", out)


class TestBlackjackSession(unittest.TestCase):
    def go(self, deck, inputs):
        with mock.patch.object(bj, "new_deck", return_value=deck):
            return play(main.run_blackjack, inputs)[1]

    def test_opening_hides_hole_card(self):
        deck = ordered([("10", "H"), ("9", "S"), ("10", "C"), ("6", "D")])
        out = self.go(deck, ["quit"])
        self.assertIn("Dealer: 10C XX (10)", out)
        self.assertIn("You:    10H 9S (19)", out)

    def test_bust_reveals_hole_card_dealer_does_not_draw(self):
        deck = ordered([("10", "H"), ("9", "S"), ("10", "C"), ("6", "D"), ("5", "S")])
        out = self.go(deck, ["hit"])
        self.assertIn("bust with 24. You lose this round.", out)
        self.assertIn("Dealer: 10C 6D (16)", out)

    def test_stand_push_round(self):
        deck = ordered([("10", "H"), ("9", "S"), ("10", "C"), ("6", "D"), ("3", "C")])
        out = self.go(deck, ["stand"])
        self.assertIn("Dealer stands on 19, you have 19 — push.", out)
        self.assertIn("Dealer: 10C 6D 3C (19)", out)

    def test_safe_hit_keeps_hole_card_hidden_and_round_continues(self):
        deck = ordered([("2", "H"), ("3", "S"), ("10", "C"), ("6", "D"), ("2", "S")])
        out = self.go(deck, ["hit", "quit"])
        self.assertIn("You draw the 2S.", out)
        self.assertEqual(out.count("XX"), 2)
        self.assertIn("You quit the round.", out)

    def test_quit_prints_quit_line(self):
        deck = ordered([("2", "H"), ("3", "S"), ("10", "C"), ("6", "D")])
        out = self.go(deck, ["quit"])
        self.assertIn("You quit the round.", out)

    def test_invalid_input_then_valid(self):
        deck = ordered([("10", "H"), ("9", "S"), ("10", "C"), ("7", "D")])
        out = self.go(deck, ["zzz", "s"])
        self.assertIn("Enter hit, stand, or quit.", out)
        self.assertIn("you win!", out)

    def test_round_ends_after_result(self):
        deck = ordered([("10", "H"), ("9", "S"), ("10", "C"), ("7", "D")])
        out = self.go(deck, ["s"])
        self.assertEqual(out.count("Hit or stand?"), 1)


class TestQuitIsCaseInsensitive(unittest.TestCase):
    def test_uppercase_quit_accepted_first_time(self):
        r, out = play(main.read_action, ["QUIT", "quit"])
        self.assertEqual(out.count("Hit or stand?"), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
