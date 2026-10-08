import unittest
from unittest import mock

import main
from helpers import play

class TestMenu(unittest.TestCase):
    def stubs(self):
        names = ["run_sudoku", "run_hangman", "run_blackjack",
                 "run_connect4", "run_battleship"]
        patches = {}
        for n in names:
            patches[n] = mock.patch.object(main, n)
        mocks = {}
        for n in names:
            mocks[n] = patches[n].start()
            self.addCleanup(patches[n].stop)
        return mocks

    def test_exit_prints_goodbye_and_stops(self):
        _, out = play(main.main, ["7"])
        self.assertIn("Thanks for playing! Goodbye.", out)
        self.assertEqual(out.count("Mini Arcade"), 1)

    def test_menu_text_matches_prd(self):
        _, out = play(main.main, ["7"])
        for line in ["||           *Mini Arcade*           ||", "1. Sudoku",
                     "2. Hangman", "3. Blackjack", "4. Connect 4",
                     "5. Battleship", "6. Give me something", "7. Exit"]:
            self.assertIn(line, out)
        self.assertIn("Enter your choice: ", out)

    def test_each_option_launches_its_game(self):
        m = self.stubs()
        order = ["run_sudoku", "run_hangman", "run_blackjack",
                 "run_connect4", "run_battleship"]
        for i in range(5):
            play(main.main, [str(i + 1), "7"])
            m[order[i]].assert_called_once()
            for other in order:
                if other != order[i]:
                    m[other].assert_not_called()
            for k in m:
                m[k].reset_mock()

    def test_menu_reprints_after_game_ends(self):
        self.stubs()
        _, out = play(main.main, ["1", "7"])
        self.assertEqual(out.count("*Mini Arcade*"), 2)

    def test_invalid_inputs_show_error_and_reprint_menu(self):
        for bad in ["abc", "0", "8", "-1", "", "2.5", "  ", "10", "one"]:
            _, out = play(main.main, [bad, "7"])
            self.assertIn("Invalid choice. Please enter a number between 1 and 7.", out)
            self.assertEqual(out.count("*Mini Arcade*"), 2)

    def test_whitespace_around_choice_is_accepted(self):
        m = self.stubs()
        play(main.main, [" 3 ", "7"])
        m["run_blackjack"].assert_called_once()

    def test_play_then_exit_sequence(self):
        m = self.stubs()
        _, out = play(main.main, ["1", "7"])
        m["run_sudoku"].assert_called_once()
        self.assertIn("Goodbye", out)

    def test_give_me_something_reaches_all_five_games(self):
        m = self.stubs()
        seen = set()
        for _ in range(300):
            main.run_random()
        for n in m:
            if m[n].called:
                seen.add(n)
        self.assertEqual(len(seen), 5)

    def test_give_me_something_via_menu_launches_exactly_one(self):
        m = self.stubs()
        play(main.main, ["6", "7"])
        total = sum(m[n].call_count for n in m)
        self.assertEqual(total, 1)

    def test_game_never_exits_app(self):
        _, out = play(main.main, ["3", "quit", "7"])
        self.assertIn("You quit the round.", out)
        self.assertIn("Goodbye", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
