import unittest

from ..jug_riddle.exceptions import InvalidAction
from ..jug_riddle.game import JugRiddle
from ..jug_riddle.types import Jug, JugAction


class TestJugRiddle(unittest.TestCase):
    def test_jug_riddle_creation(self):
        # Test creating a JugRiddle instance
        jug_riddle = JugRiddle(4, 3, 2)
        self.assertEqual(jug_riddle.jug_1_capacity, 4)
        self.assertEqual(jug_riddle.jug_2_capacity, 3)
        self.assertEqual(jug_riddle.goal, 2)
        self.assertEqual(len(jug_riddle), 0)  # No actions taken yet

    def test_fill_empty_actions(self):
        # Test filling and emptying actions
        jug_riddle = JugRiddle(4, 3, 2)

        # Filling Jug 1
        jug_riddle.take_action(Jug.JUG_1, JugAction.FILL)
        self.assertEqual(jug_riddle.state.jug_1, 4)

        # Emptying Jug 1
        jug_riddle.take_action(Jug.JUG_1, JugAction.EMPTY)
        self.assertEqual(jug_riddle.state.jug_1, 0)

    def test_no_emptying_empty_jugs(self):
        jug_riddle = JugRiddle(4, 3, 2)

        self.assertEqual(jug_riddle.state.jug_1, 0)
        # Attempt to empty the jug 1 that is already empty (should raise InvalidAction)
        with self.assertRaises(InvalidAction):
            jug_riddle.take_action(Jug.JUG_1, JugAction.EMPTY)

    def test_no_consecutive_fills(self):
        jug_riddle = JugRiddle(4, 3, 2)

        # Filling Jug 1
        jug_riddle.take_action(Jug.JUG_1, JugAction.FILL)
        # Attempt to fill the jug again (should raise InvalidAction)
        with self.assertRaises(InvalidAction):
            jug_riddle.take_action(Jug.JUG_1, JugAction.FILL)

    def test_transfer_action(self):
        # Test transfer action
        jug_riddle = JugRiddle(4, 3, 2)

        # Filling Jug 1
        jug_riddle.take_action(Jug.JUG_1, JugAction.FILL)

        # Transferring from Jug 1 to Jug 2
        jug_riddle.take_action(Jug.JUG_1, JugAction.TRANSFER)
        self.assertEqual(jug_riddle.state.jug_1, 1)
        self.assertEqual(jug_riddle.state.jug_2, 3)

        # Now we empty the jug 1 and try to transfer again
        jug_riddle.take_action(Jug.JUG_1, JugAction.EMPTY)
        self.assertEqual(jug_riddle.state.jug_1, 0)
        # Attempt to transfer from an empty jug (should raise InvalidAction)
        with self.assertRaises(InvalidAction):
            jug_riddle.take_action(Jug.JUG_1, JugAction.TRANSFER)

    def test_goal_achievement(self):
        # Test achieving the goal
        jug_riddle = JugRiddle(4, 2, 2)

        # Fill Jug 1 and transfer to Jug 2 to achieve the goal
        jug_riddle.take_action(Jug.JUG_1, JugAction.FILL)
        jug_riddle.take_action(Jug.JUG_1, JugAction.TRANSFER)
        jug_riddle.take_action(Jug.JUG_1, JugAction.EMPTY)

        self.assertTrue(jug_riddle.done)
        self.assertEqual(jug_riddle.state.total_water, 2)
        self.assertEqual(
            jug_riddle.view_solution(),
            "Step 1: FILL JUG 1\nStep 2: TRANSFER JUG 1\nStep 3: EMPTY JUG 1",
        )

    def test_almost_done_game(self):
        # Test the finish_almost_done_game method
        jug_riddle = JugRiddle(4, 3, 1)

        # Fill Jug 1 to almost achieve the goal
        jug_riddle.take_action(Jug.JUG_1, JugAction.FILL)
        jug_riddle.take_action(Jug.JUG_1, JugAction.TRANSFER)
        self.assertTrue(jug_riddle.almost_done)
        jug_riddle.finish_almost_done_game()

        self.assertTrue(jug_riddle.done)
        self.assertEqual(
            jug_riddle.view_solution(),
            "Step 1: FILL JUG 1\nStep 2: TRANSFER JUG 1\nStep 3: EMPTY JUG 2",
        )
