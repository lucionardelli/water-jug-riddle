import unittest

from ..jug_riddle import Jug, JugAction, JugRiddle, UnsolvableRiddle, solve


class TestJugRiddleSolver(unittest.TestCase):
    def test_solve_solvable_riddle(self):
        # Test solving a solvable riddle
        riddle = JugRiddle(4, 3, 2)
        solution = solve(riddle)
        self.assertTrue(solution.done)
        self.assertEqual(solution.state.total_water, 2)

    def test_solve_unsolvable_riddle(self):
        # Test solving an unsolvable riddle
        riddle = JugRiddle(6, 4, 3)
        with self.assertRaises(UnsolvableRiddle):
            solve(riddle)

    def test_solve_complex_riddle(self):
        # Test solving a riddle with jugs of size 7 and 4, goal = 3
        riddle = JugRiddle(7, 4, 3)
        solution = solve(riddle)

        # Verify the solution state and actions
        self.assertTrue(solution.done)
        self.assertEqual(solution.state.total_water, 3)

        # Verify the sequence of actions
        expected_actions = [
            (JugAction.FILL, Jug.JUG_1),  # Fill Jug 1
            (JugAction.TRANSFER, Jug.JUG_1),  # Transfer from Jug 1 to Jug 2
            (JugAction.EMPTY, Jug.JUG_2),  # Empty Jug 2
        ]

        self.assertEqual(solution._actions, expected_actions)
