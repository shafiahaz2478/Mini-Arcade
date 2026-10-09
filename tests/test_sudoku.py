import unittest
from unittest import mock

import main
import sudoku_logic as sd
from helpers import play

def solved_grid_ok(g):
    full = set(range(1, 10))
    for r in range(9):
        if set(g[r]) != full:
            return False
    for c in range(9):
        if set(g[r][c] for r in range(9)) != full:
            return False
    for br in (0, 3, 6):
        for bc in (0, 3, 6):
            cells = set(g[br + i][bc + j] for i in range(3) for j in range(3))
            if cells != full:
                return False
    return True


class TestSudokuLogic(unittest.TestCase):
    def test_base_solution_is_valid(self):
        self.assertTrue(solved_grid_ok(sd.BASE_SOLUTION))

    def test_random_solution_always_valid(self):
        for _ in range(100):
            self.assertTrue(solved_grid_ok(sd.random_solution()))

    def test_random_solution_does_not_mutate_base(self):
        before = [row[:] for row in sd.BASE_SOLUTION]
        sd.random_solution()
        self.assertEqual(before, sd.BASE_SOLUTION)

    def test_new_puzzle_removes_48_cells(self):
        board, givens = sd.new_puzzle()
        zeros = sum(row.count(0) for row in board)
        self.assertEqual(zeros, 48)
        self.assertEqual(len(givens), 33)

    def test_givens_match_nonzero_cells(self):
        board, givens = sd.new_puzzle()
        for r in range(9):
            for c in range(9):
                self.assertEqual((r, c) in givens, board[r][c] != 0)

    def test_puzzle_has_no_duplicates_anywhere(self):
        board, _ = sd.new_puzzle()
        for r in range(9):
            for c in range(9):
                if board[r][c] != 0:
                    self.assertTrue(sd.is_valid_placement(board, r, c, board[r][c]))

    def test_consecutive_puzzles_differ(self):
        a, _ = sd.new_puzzle()
        b, _ = sd.new_puzzle()
        self.assertNotEqual(a, b)

    def empty(self):
        return [[0] * 9 for _ in range(9)]

    def test_placement_row_conflict(self):
        b = self.empty()
        b[0][0] = 5
        self.assertFalse(sd.is_valid_placement(b, 0, 8, 5))

    def test_placement_column_conflict(self):
        b = self.empty()
        b[0][0] = 5
        self.assertFalse(sd.is_valid_placement(b, 8, 0, 5))

    def test_placement_box_conflict(self):
        b = self.empty()
        b[0][0] = 5
        self.assertFalse(sd.is_valid_placement(b, 2, 2, 5))

    def test_placement_legal(self):
        b = self.empty()
        b[0][0] = 5
        self.assertTrue(sd.is_valid_placement(b, 4, 4, 5))
        self.assertTrue(sd.is_valid_placement(b, 4, 4, 6))

    def test_placement_ignores_target_cell(self):
        b = self.empty()
        b[3][3] = 7
        self.assertTrue(sd.is_valid_placement(b, 3, 3, 7))

    def test_box_boundaries(self):
        b = self.empty()
        b[2][2] = 9
        self.assertTrue(sd.is_valid_placement(b, 3, 3, 9))
        self.assertFalse(sd.is_valid_placement(b, 0, 0, 9))

    def test_make_move_writes_and_returns_board(self):
        b = self.empty()
        r = sd.make_move(b, 4, 5, 8)
        self.assertEqual(r[4][5], 8)

    def test_correction_overwrites_own_entry(self):
        b = self.empty()
        sd.make_move(b, 0, 0, 3)
        self.assertTrue(sd.is_valid_placement(b, 0, 0, 4))
        sd.make_move(b, 0, 0, 4)
        self.assertEqual(b[0][0], 4)

    def test_game_state_in_progress(self):
        b = [row[:] for row in sd.BASE_SOLUTION]
        b[0][0] = 0
        self.assertEqual(sd.game_state(b), "in progress")

    def test_game_state_solved(self):
        self.assertEqual(sd.game_state([row[:] for row in sd.BASE_SOLUTION]),
                         "Solved! Well played.")

    def test_render_structure(self):
        board, givens = sd.new_puzzle()
        lines = sd.render_board(board, givens).split("\n")
        self.assertEqual(len(lines), 12)
        self.assertEqual(lines[0].replace("|", " ").split(), list("123456789"))
        seps = [l for l in lines if set(l.strip()) <= set("-+") and l.strip()]
        self.assertEqual(len(seps), 2)

    def test_render_cell_styles(self):
        b = self.empty()
        b[0][0] = 5
        b[0][1] = 6
        out = sd.render_board(b, {(0, 0)})
        row1 = out.split("\n")[1]
        self.assertIn(" 5 ", row1)
        self.assertIn("[6]", row1)
        self.assertIn(" . ", row1)
        self.assertNotIn("[5]", row1)

    def test_render_row_labels(self):
        board, givens = sd.new_puzzle()
        lines = [l for l in sd.render_board(board, givens).split("\n")[1:]
                 if "-" not in l]
        for i, l in enumerate(lines):
            self.assertEqual(l.split()[0], str(i + 1))


class TestSudokuInput(unittest.TestCase):
    def setUp(self):
        self.b = [[0] * 9 for _ in range(9)]
        self.b[0][0] = 5
        self.givens = {(0, 0)}

    def test_valid_move_is_zero_indexed(self):
        r, _ = play(main.read_move, ["5 5 3"], self.b, self.givens)
        self.assertEqual(r, (4, 4, 3))

    def test_quit(self):
        r, _ = play(main.read_move, [" quit "], self.b, self.givens)
        self.assertEqual(r, "quit")

    def test_bad_shapes_are_reasked(self):
        bad = ["", "1 2", "1 2 3 4", "a b c", "0 1 1", "10 1 1", "1 0 1",
               "1 10 1", "1 1 10", "1.5 2 3", "-1 2 3"]
        for item in bad:
            r, out = play(main.read_move, [item, "5 5 3"], self.b, self.givens)
            self.assertEqual(r, (4, 4, 3))
            self.assertIn("Enter three numbers", out)

    def test_given_cell_rejected(self):
        r, out = play(main.read_move, ["1 1 9", "5 5 3"], self.b, self.givens)
        self.assertIn("That cell is part of the puzzle — it can't be changed.", out)
        self.assertEqual(r, (4, 4, 3))

    def test_illegal_placement_rejected_with_message(self):
        r, out = play(main.read_move, ["1 5 5", "5 5 3"], self.b, self.givens)
        self.assertIn("5 doesn't fit there — its row, column, or box already has a 5.", out)
        self.assertEqual(r, (4, 4, 3))

    def test_prompt_text(self):
        _, out = play(main.read_move, ["quit"], self.b, self.givens)
        self.assertIn("Row, column, value (0 erases, or 'quit'): ", out)

    def test_error_text(self):
        _, out = play(main.read_move, ["x", "quit"], self.b, self.givens)
        self.assertIn("Enter three numbers: row 1-9, column 1-9, value 0-9.", out)

    def test_value_zero_erases(self):
        r, _ = play(main.read_move, ["5 5 0"], self.b, self.givens)
        self.assertEqual(r, (4, 4, 0))

    def test_erasing_a_given_is_rejected(self):
        r, out = play(main.read_move, ["1 1 0", "quit"], self.b, self.givens)
        self.assertEqual(r, "quit")
        self.assertIn("That cell is part of the puzzle", out)


class TestSudokuSession(unittest.TestCase):
    def almost_done(self):
        b = [row[:] for row in sd.BASE_SOLUTION]
        b[0][0] = 0
        g = {(r, c) for r in range(9) for c in range(9)} - {(0, 0)}
        return b, g

    def test_solving_last_cell_ends_with_solved_line(self):
        with mock.patch.object(sd, "new_puzzle", return_value=self.almost_done()):
            _, out = play(main.run_sudoku, ["1 1 5"])
        self.assertIn("Solved! Well played.", out)
        self.assertEqual(out.count("Row, column, value"), 1)

    def test_final_board_shown_before_solved_line(self):
        with mock.patch.object(sd, "new_puzzle", return_value=self.almost_done()):
            _, out = play(main.run_sudoku, ["1 1 5"])
        self.assertLess(out.index("[5]"), out.index("Solved!"))

    def test_quit_line(self):
        with mock.patch.object(sd, "new_puzzle", return_value=self.almost_done()):
            _, out = play(main.run_sudoku, ["quit"])
        self.assertIn("You quit this puzzle.", out)
        self.assertNotIn("Solved", out)

    def test_wrong_then_corrected_entry_still_solves(self):
        b, g = self.almost_done()
        b[0][1] = 0
        g.discard((0, 1))
        with mock.patch.object(sd, "new_puzzle", return_value=(b, g)):
            _, out = play(main.run_sudoku, ["1 1 5", "1 2 3"])
        self.assertIn("Solved! Well played.", out)

    def test_board_reprinted_every_turn(self):
        b, g = self.almost_done()
        b[0][1] = 0
        g.discard((0, 1))
        with mock.patch.object(sd, "new_puzzle", return_value=(b, g)):
            _, out = play(main.run_sudoku, ["1 1 5", "quit"])
        self.assertEqual(out.count("Row, column, value"), 2)
        self.assertIn("[5]", out)


class TestQuitIsCaseInsensitive(unittest.TestCase):
    def test_uppercase_quit_accepted_first_time(self):
        r, out = play(main.read_move, ["QUIT", "quit"], [[0] * 9 for _ in range(9)], set())
        self.assertEqual(out.count("Row, column, value"), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
