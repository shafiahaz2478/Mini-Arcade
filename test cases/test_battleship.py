import unittest
from unittest import mock

import battleship_logic as bs
import main
from helpers import play

class TestBattleshipLogic(unittest.TestCase):
    def contiguous_line(self, cells):
        rows = set(r for r, c in cells)
        cols = set(c for r, c in cells)
        if len(rows) == 1:
            cs = sorted(cols)
            return cs == list(range(cs[0], cs[0] + len(cs)))
        if len(cols) == 1:
            rs = sorted(rows)
            return rs == list(range(rs[0], rs[0] + len(rs)))
        return False

    def test_fleet_composition(self):
        for _ in range(200):
            f = bs.place_fleet()
            self.assertEqual([(n, len(c)) for n, c in f], bs.SHIPS)

    def test_fleet_on_grid_no_overlap_straight(self):
        for _ in range(200):
            f = bs.place_fleet()
            seen = set()
            for n, cells in f:
                for r, c in cells:
                    self.assertTrue(0 <= r < 10 and 0 <= c < 10)
                self.assertTrue(self.contiguous_line(cells))
                self.assertFalse(seen & cells)
                seen |= cells
            self.assertEqual(len(seen), 17)

    def test_fleets_vary(self):
        self.assertNotEqual(bs.place_fleet(), bs.place_fleet())

    def test_is_sunk(self):
        self.assertTrue(bs.is_sunk({(0, 0), (0, 1)}, {(0, 0), (0, 1), (5, 5)}))
        self.assertFalse(bs.is_sunk({(0, 0), (0, 1)}, {(0, 0)}))
        self.assertFalse(bs.is_sunk({(0, 0), (0, 1)}, set()))

    fleet = [("Destroyer", {(0, 0), (0, 1)}), ("Cruiser", {(5, 5), (5, 6), (5, 7)})]

    def test_make_move_miss(self):
        r = bs.make_move(self.fleet, set(), 9, 9)
        self.assertEqual(r[-1], "Miss.")
        self.assertIn((9, 9), r[0])

    def test_make_move_hit(self):
        r = bs.make_move(self.fleet, set(), 0, 0)
        self.assertEqual(r[-1], "Hit!")

    def test_make_move_sink(self):
        r = bs.make_move(self.fleet, {(0, 0)}, 0, 1)
        self.assertEqual(r[-1], "Hit — you sank the enemy Destroyer!")

    def test_make_move_returns_shots_outcome_report(self):
        r = bs.make_move(self.fleet, set(), 9, 9)
        self.assertEqual(len(r), 3)
        self.assertEqual(r[1], "miss")
        self.assertEqual(bs.make_move(self.fleet, set(), 0, 0)[1], "hit")

    def test_computer_fire_never_repeats_and_covers_grid(self):
        f = bs.place_fleet()
        shots = set()
        for i in range(100):
            before = len(shots)
            shots, *_ = bs.computer_fire(f, shots)
            self.assertEqual(len(shots), before + 1)
        self.assertEqual(len(shots), 100)

    def fire_at(self, fleet, shots, row, col):
        with mock.patch.object(bs.random, "randrange", side_effect=[row, col]):
            return bs.computer_fire(fleet, shots)

    def test_computer_fire_hit_report(self):
        f = [("Destroyer", {(0, 0), (0, 1)})]
        r = self.fire_at(f, set(), 0, 0)
        self.assertEqual(r[-1], "The computer fires at 1 1 — a hit!")
        self.assertEqual(r[1], "hit")

    def test_computer_fire_sink_report(self):
        f = [("Destroyer", {(0, 0), (0, 1)})]
        r = self.fire_at(f, {(0, 0)}, 0, 1)
        self.assertEqual(r[-1], "The computer fires at 1 2 — it sinks your Destroyer!")

    def test_computer_fire_miss_report(self):
        f = [("Destroyer", {(0, 0), (0, 1)})]
        r = self.fire_at(f, set(), 9, 9)
        self.assertEqual(r[-1], "The computer fires at 10 10 — a miss.")
        self.assertEqual(r[1], "miss")

    def test_render_player_board_symbols(self):
        f = [("Destroyer", {(0, 0), (0, 1)})]
        out = bs.render_player_board(f, {(0, 0), (3, 3)})
        lines = out.split("\n")
        self.assertEqual(len(lines), 11)
        self.assertEqual(lines[1].split()[1:3], ["X", "#"])
        self.assertEqual(lines[4].split()[4], "o")
        self.assertIn(".", lines[2])

    def test_render_enemy_board_hides_ships(self):
        f = [("Destroyer", {(0, 0), (0, 1)})]
        out = bs.render_enemy_board(f, set())
        self.assertNotIn("#", out)
        self.assertNotIn("X", out)
        self.assertNotIn("*", out)

    def test_render_enemy_board_symbols(self):
        f = [("Destroyer", {(0, 0), (0, 1)}), ("Cruiser", {(5, 5), (5, 6), (5, 7)})]
        out = bs.render_enemy_board(f, {(0, 0), (0, 1), (5, 5), (9, 9)})
        lines = out.split("\n")
        self.assertEqual(lines[1].split()[1:3], ["*", "*"])
        self.assertEqual(lines[6].split()[6], "X")
        self.assertEqual(lines[10].split()[-1], "o")

    def test_render_headers_and_labels(self):
        out = bs.render_enemy_board(bs.place_fleet(), set()).split("\n")
        self.assertEqual(out[0].split(), [str(n) for n in range(1, 11)])
        for i in range(10):
            self.assertEqual(out[i + 1].split()[0], str(i + 1))

    def test_game_state(self):
        ef = [("D", {(0, 0), (0, 1)})]
        pf = [("D", {(5, 5), (5, 6)})]
        self.assertEqual(bs.game_state(ef, set(), pf, set()), "in progress")
        self.assertEqual(bs.game_state(ef, {(0, 0), (0, 1)}, pf, set()),
                         "You win — the enemy fleet is destroyed!")
        self.assertEqual(bs.game_state(ef, set(), pf, {(5, 5), (5, 6)}),
                         "You lose — your fleet is destroyed!")

    def test_game_state_needs_all_ships_sunk(self):
        ef = [("A", {(0, 0)}), ("B", {(1, 1)})]
        self.assertEqual(bs.game_state(ef, {(0, 0)}, [("P", {(9, 9)})], set()),
                         "in progress")


class TestBattleshipInput(unittest.TestCase):
    def test_valid_zero_indexed(self):
        r, _ = play(main.read_coords, ["3 4"], set())
        self.assertEqual(r, (2, 3))

    def test_corners_and_whitespace(self):
        for raw, want in [("1 1", (0, 0)), ("10 10", (9, 9)), ("  5   6 ", (4, 5))]:
            r, _ = play(main.read_coords, [raw], set())
            self.assertEqual(r, want)

    def test_quit(self):
        r, _ = play(main.read_coords, ["quit"], set())
        self.assertEqual(r, "quit")

    def test_invalid_reasked(self):
        for bad in ["", "1", "1 2 3", "0 1", "1 0", "11 1", "1 11", "a b",
                    "-1 5", "1.5 2", "3,4"]:
            r, out = play(main.read_coords, [bad, "2 2"], set())
            self.assertEqual(r, (1, 1))
            self.assertIn("Enter two numbers 1-10: row and column.", out)

    def test_already_fired(self):
        r, out = play(main.read_coords, ["3 4", "1 1"], {(2, 3)})
        self.assertEqual(r, (0, 0))
        self.assertIn("You already fired at 3 4.", out)

    def test_prompt(self):
        _, out = play(main.read_coords, ["1 1"], set())
        self.assertIn("Fire at row, column (or 'quit'): ", out)


class TestBattleshipSession(unittest.TestCase):
    def fleets(self):
        player = [("Destroyer", {(5, 5), (5, 6)})]
        enemy = [("Destroyer", {(0, 0), (0, 1)})]
        return mock.patch.object(bs, "place_fleet", side_effect=[player, enemy])

    def test_two_boards_shown_each_turn(self):
        with self.fleets():
            _, out = play(main.run_battleship, ["quit"])
        self.assertEqual(out.count("1 2 3 4 5 6 7 8 9 10"), 2)

    def test_quit_line(self):
        with self.fleets():
            _, out = play(main.run_battleship, ["quit"])
        self.assertIn("You quit the battle.", out)

    def test_win_by_sinking_fleet(self):
        stub = mock.Mock(side_effect=lambda pf, cs: (cs | {(9, 9)}, "miss",
                         "The computer fires at 10 10 — a miss."))
        with self.fleets(), mock.patch.object(bs, "computer_fire", stub):
            _, out = play(main.run_battleship, ["1 1", "1 2"])
        self.assertIn("You win — the enemy fleet is destroyed!", out)

    def test_loss_when_player_fleet_destroyed(self):
        def sink(pf, cs):
            cs |= {(5, 5), (5, 6)}
            return cs, "hit", "The computer fires at 6 6 — it sinks your Destroyer!"

        with self.fleets(), mock.patch.object(bs, "computer_fire", sink):
            _, out = play(main.run_battleship, ["10 10", "10 9", "10 8"])
        self.assertIn("You lose — your fleet is destroyed!", out)

    def test_computer_fires_after_player_miss(self):
        stub = mock.Mock(side_effect=lambda pf, cs: (cs | {(9, 9)}, "miss",
                         "The computer fires at 10 10 — a miss."))
        with self.fleets(), mock.patch.object(bs, "computer_fire", stub):
            _, out = play(main.run_battleship, ["10 10", "quit"])
        self.assertEqual(stub.call_count, 1)
        self.assertIn("The computer fires at 10 10 — a miss.", out)

    def test_hit_gives_extra_shot_computer_waits(self):
        stub = mock.Mock(side_effect=lambda pf, cs: (cs | {(9, 9)}, "miss",
                         "The computer fires at 10 10 — a miss."))
        with self.fleets(), mock.patch.object(bs, "computer_fire", stub):
            _, out = play(main.run_battleship, ["1 1", "quit"])
        self.assertEqual(stub.call_count, 0)
        self.assertEqual(out.count("Fire at row, column"), 2)

    def test_win_checked_before_computer_fires(self):
        stub = mock.Mock()
        with self.fleets(), mock.patch.object(bs, "computer_fire", stub):
            play(main.run_battleship, ["1 1", "1 2"])
        stub.assert_not_called()

    def test_reports_printed(self):
        stub = mock.Mock(side_effect=lambda pf, cs: (cs | {(9, 9)}, "miss",
                         "The computer fires at 10 10 — a miss."))
        with self.fleets(), mock.patch.object(bs, "computer_fire", stub):
            _, out = play(main.run_battleship, ["1 1", "10 10", "quit"])
        self.assertIn("Hit!", out)
        self.assertIn("Miss.", out)

    def test_repeat_shot_rejected_in_session(self):
        stub = mock.Mock(side_effect=lambda pf, cs: (cs | {(9, 9)}, "miss",
                         "The computer fires at 10 10 — a miss."))
        with self.fleets(), mock.patch.object(bs, "computer_fire", stub):
            _, out = play(main.run_battleship, ["10 10", "10 10", "quit"])
        self.assertIn("You already fired at 10 10.", out)


class TestQuitIsCaseInsensitive(unittest.TestCase):
    def test_uppercase_quit_accepted_first_time(self):
        r, out = play(main.read_coords, ["QUIT", "quit"], set())
        self.assertEqual(out.count("Fire at row, column"), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
