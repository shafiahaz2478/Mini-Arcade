import random
import unittest

import connect4_logic as c4
import main
from helpers import play

class TestConnect4Logic(unittest.TestCase):
    def test_new_board(self):
        b = c4.new_board()
        self.assertEqual(len(b), 6)
        for row in b:
            self.assertEqual(row, ["."] * 7)

    def test_rows_are_independent_lists(self):
        b = c4.new_board()
        b[0][0] = "X"
        self.assertEqual(b[1][0], ".")

    def test_render_header_and_orientation(self):
        b = c4.new_board()
        c4.make_move(b, 0, "X")
        lines = c4.render(b).split("\n")
        self.assertEqual(lines[0], "1 2 3 4 5 6 7")
        self.assertEqual(len(lines), 7)
        self.assertEqual(lines[-1], "X . . . . . .")
        self.assertEqual(lines[1], ". . . . . . .")

    def test_gravity_stacks(self):
        b = c4.new_board()
        c4.make_move(b, 3, "X")
        c4.make_move(b, 3, "O")
        self.assertEqual(b[0][3], "X")
        self.assertEqual(b[1][3], "O")

    def test_column_full_after_six(self):
        b = c4.new_board()
        for i in range(6):
            self.assertFalse(c4.column_is_full(b, 2))
            c4.make_move(b, 2, "X" if i % 2 == 0 else "O")
        self.assertTrue(c4.column_is_full(b, 2))
        self.assertFalse(c4.column_is_full(b, 3))

    def test_horizontal_win(self):
        b = c4.new_board()
        for c in range(4):
            b[0][c] = "X"
        self.assertEqual(c4.game_state(b), "Player X wins!")

    def test_vertical_win(self):
        b = c4.new_board()
        for r in range(4):
            b[r][6] = "O"
        self.assertEqual(c4.game_state(b), "Player O wins!")

    def test_diagonal_up_right_win(self):
        b = c4.new_board()
        for i in range(4):
            b[i][i] = "X"
        self.assertEqual(c4.game_state(b), "Player X wins!")

    def test_diagonal_up_left_win(self):
        b = c4.new_board()
        for i in range(4):
            b[i][6 - i] = "O"
        self.assertEqual(c4.game_state(b), "Player O wins!")

    def test_win_at_board_edges(self):
        b = c4.new_board()
        for c in range(3, 7):
            b[5][c] = "X"
        self.assertEqual(c4.game_state(b), "Player X wins!")

    def test_three_in_a_row_is_not_a_win(self):
        b = c4.new_board()
        for c in range(3):
            b[0][c] = "X"
        self.assertEqual(c4.game_state(b), "in progress")

    def test_broken_line_is_not_a_win(self):
        b = c4.new_board()
        for c, m in zip(range(4), "XXOX"):
            b[0][c] = m
        self.assertEqual(c4.game_state(b), "in progress")

    def test_empty_board_in_progress(self):
        self.assertEqual(c4.game_state(c4.new_board()), "in progress")

    def test_draw(self):
        b = [["X" if ((r // 2) + c) % 2 == 0 else "O" for c in range(7)]
             for r in range(6)]
        self.assertEqual(c4.game_state(b), "The board is full — a draw.")

    def test_win_on_full_board_beats_draw(self):
        b = [["X" if ((r // 2) + c) % 2 == 0 else "O" for c in range(7)]
             for r in range(6)]
        for c in range(4):
            b[0][c] = "X"
        self.assertEqual(c4.game_state(b), "Player X wins!")


class TestConnect4Input(unittest.TestCase):
    def test_valid_columns_zero_indexed(self):
        for n in range(1, 8):
            r, _ = play(main.read_column, [str(n)], c4.new_board(), "X")
            self.assertEqual(r, n - 1)

    def test_whitespace(self):
        r, _ = play(main.read_column, [" 4 "], c4.new_board(), "X")
        self.assertEqual(r, 3)

    def test_quit(self):
        r, _ = play(main.read_column, ["quit"], c4.new_board(), "O")
        self.assertEqual(r, "quit")

    def test_invalid_inputs(self):
        for bad in ["0", "8", "abc", "", "1.5", "-1", "10", "1 2"]:
            r, out = play(main.read_column, [bad, "2"], c4.new_board(), "X")
            self.assertEqual(r, 1)
            self.assertIn("Enter a column number 1-7.", out)

    def test_full_column_rejected(self):
        b = c4.new_board()
        for i in range(6):
            c4.make_move(b, 0, "X" if i % 2 == 0 else "O")
        r, out = play(main.read_column, ["1", "2"], b, "X")
        self.assertEqual(r, 1)
        self.assertIn("Column 1 is full — choose another.", out)

    def test_prompt_names_player(self):
        _, out = play(main.read_column, ["1"], c4.new_board(), "O")
        self.assertIn("Player O, choose a column (1-7 or 'quit'): ", out)


class TestConnect4Session(unittest.TestCase):
    def test_x_wins_vertically(self):
        _, out = play(main.run_connect4, ["1", "2", "1", "2", "1", "2", "1"])
        self.assertIn("Player X wins!", out)

    def test_o_wins_vertically(self):
        _, out = play(main.run_connect4, ["1", "2", "1", "2", "3", "2", "3", "2"])
        self.assertIn("Player O wins!", out)
        self.assertNotIn("Player X wins!", out)

    def test_turns_alternate_and_x_first(self):
        _, out = play(main.run_connect4, ["1", "quit"])
        self.assertIn("Player X, choose", out)
        self.assertIn("Player O, choose", out)
        self.assertIn("Player O quits the game.", out)

    def test_quit_first_turn_names_x(self):
        _, out = play(main.run_connect4, ["quit"])
        self.assertIn("Player X quits the game.", out)

    def test_final_board_shown_with_winner(self):
        _, out = play(main.run_connect4, ["1", "2", "1", "2", "1", "2", "1"])
        self.assertLess(out.rindex("1 2 3 4 5 6 7"), out.index("Player X wins!"))

    def find_draw(self):
        rng = random.Random(0)
        for _ in range(200000):
            b = c4.new_board()
            mark = "X"
            moves = []
            while True:
                cols = [c for c in range(7) if not c4.column_is_full(b, c)]
                c = rng.choice(cols)
                c4.make_move(b, c, mark)
                moves.append(c)
                st = c4.game_state(b)
                if st != "in progress":
                    break
                mark = "O" if mark == "X" else "X"
            if "draw" in st:
                return moves
        return None

    def test_draw_game_full_playthrough(self):
        moves = self.find_draw()
        self.assertIsNotNone(moves)
        self.assertEqual(len(moves), 42)
        _, out = play(main.run_connect4, [str(c + 1) for c in moves])
        self.assertIn("The board is full — a draw.", out)


class TestQuitIsCaseInsensitive(unittest.TestCase):
    def test_uppercase_quit_accepted_first_time(self):
        r, out = play(main.read_column, ["QUIT", "quit"], c4.new_board(), "X")
        self.assertEqual(out.count("choose a column"), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
