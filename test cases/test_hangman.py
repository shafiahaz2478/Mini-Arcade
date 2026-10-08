import unittest
from unittest import mock

import hangman_logic as hm
import main
from helpers import play

class TestHangmanLogic(unittest.TestCase):
    def test_wordlist_rules(self):
        self.assertEqual(len(hm.WORDLIST), 10)
        for w in hm.WORDLIST:
            self.assertTrue(4 <= len(w) <= 8)
            self.assertTrue(w.isalpha() and w.islower() and w.isascii())

    def test_pick_word_from_list(self):
        for _ in range(50):
            self.assertIn(hm.pick_word(), hm.WORDLIST)

    def test_seven_gallows(self):
        self.assertEqual(len(hm.GALLOWS), 7)
        self.assertEqual(len(set(hm.GALLOWS)), 7)

    def test_gallows_index(self):
        self.assertEqual(hm.draw_gallows(6), hm.GALLOWS[0])
        self.assertEqual(hm.draw_gallows(5), hm.GALLOWS[1])
        self.assertEqual(hm.draw_gallows(0), hm.GALLOWS[6])

    def test_gallows_first_has_no_figure_last_is_complete(self):
        self.assertNotIn("O", hm.draw_gallows(6))
        last = hm.draw_gallows(0)
        for part in ["O", "/", "\\"]:
            self.assertIn(part, last)

    def test_mask_example_from_design_doc(self):
        self.assertEqual(hm.mask_word("python", {"t"}), "_ _ t _ _ _")

    def test_mask_empty_and_full(self):
        self.assertEqual(hm.mask_word("loop", set()), "_ _ _ _")
        self.assertEqual(hm.mask_word("loop", set("lop")), "l o o p")

    def test_mask_repeated_letters_all_shown(self):
        self.assertEqual(hm.mask_word("loop", {"o"}), "_ o o _")

    def test_hit_keeps_lives(self):
        g, l, rep = hm.make_move("python", set(), 6, "p")
        self.assertEqual(l, 6)
        self.assertIn("p", g)
        self.assertEqual(rep, "Yes! 'p' is in the word.")

    def test_miss_costs_one_life(self):
        g, l, rep = hm.make_move("python", set(), 6, "z")
        self.assertEqual(l, 5)
        self.assertEqual(rep, "Nope, 'z' is not in the word.")

    def test_repeated_letter_word_counts_one_hit(self):
        g, l, rep = hm.make_move("loop", set(), 6, "o")
        self.assertEqual(l, 6)

    def test_state_won(self):
        self.assertEqual(hm.game_state("loop", set("lop"), 3),
                         "You won! The word was 'loop'.")

    def test_state_lost(self):
        self.assertEqual(hm.game_state("loop", {"l"}, 0),
                         "You lost! The word was 'loop'.")

    def test_state_in_progress(self):
        self.assertEqual(hm.game_state("loop", {"l"}, 4), "in progress")

    def test_won_checked_before_lost(self):
        self.assertTrue(hm.game_state("loop", set("lop"), 0).startswith("You won"))


class TestHangmanInput(unittest.TestCase):
    def test_valid_letter(self):
        r, _ = play(main.read_letter, ["a"], set())
        self.assertEqual(r, "a")

    def test_uppercase_and_spaces_normalised(self):
        r, _ = play(main.read_letter, ["  Q "], set())
        self.assertEqual(r, "q")

    def test_quit(self):
        r, _ = play(main.read_letter, ["quit"], set())
        self.assertEqual(r, "quit")

    def test_q_is_a_legal_guess(self):
        r, _ = play(main.read_letter, ["q"], set())
        self.assertEqual(r, "q")

    def test_invalid_inputs_reasked_with_exact_message(self):
        for bad in ["", "ab", "1", "é", "!", "  ", "a b"]:
            r, out = play(main.read_letter, [bad, "z"], set())
            self.assertEqual(r, "z")
            self.assertIn("Please enter a single letter (a-z).", out)

    def test_repeat_guess_message(self):
        r, out = play(main.read_letter, ["x", "y"], {"x"})
        self.assertEqual(r, "y")
        self.assertIn("You already guessed 'x'.", out)

    def test_prompt_text(self):
        _, out = play(main.read_letter, ["a"], set())
        self.assertIn("Guess a letter (or 'quit' to quit): ", out)


class TestHangmanSession(unittest.TestCase):
    def run_word(self, word, inputs):
        with mock.patch.object(hm, "pick_word", return_value=word):
            return play(main.run_hangman, inputs)[1]

    def test_win(self):
        out = self.run_word("loop", ["l", "o", "p"])
        self.assertIn("You won! The word was 'loop'.", out)

    def test_loss_after_six_misses(self):
        out = self.run_word("loop", list("abcdef"))
        self.assertIn("You lost! The word was 'loop'.", out)

    def test_five_misses_not_a_loss(self):
        out = self.run_word("loop", list("abcde") + ["quit"])
        self.assertNotIn("You lost", out)
        self.assertIn("You quit. The word was 'loop'.", out)

    def test_quit_reveals_word(self):
        out = self.run_word("python", ["quit"])
        self.assertIn("You quit. The word was 'python'.", out)

    def test_invalid_and_repeat_input_cost_no_life(self):
        out = self.run_word("loop", ["1", "z", "z", "!", "l", "o", "p"])
        self.assertIn("You won!", out)
        self.assertEqual(out.count("Nope"), 1)

    def test_lives_never_printed_as_number(self):
        out = self.run_word("loop", ["z", "quit"])
        self.assertNotIn("lives", out.lower())

    def test_display_before_every_prompt(self):
        out = self.run_word("loop", ["l", "quit"])
        self.assertEqual(out.count("_ _ _ _"), 1)
        self.assertIn("l _ _ _", out)

    def test_report_printed_each_turn(self):
        out = self.run_word("loop", ["l", "z", "quit"])
        self.assertIn("Yes! 'l' is in the word.", out)
        self.assertIn("Nope, 'z' is not in the word.", out)


class TestQuitIsCaseInsensitive(unittest.TestCase):
    def test_uppercase_quit_accepted_first_time(self):
        r, out = play(main.read_letter, ["QUIT", "quit"], set())
        self.assertEqual(out.count("Guess a letter"), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
