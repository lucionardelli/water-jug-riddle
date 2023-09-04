"""
To solve the riddle, we will use a mathematical approach.

Let X and Y be the volumes of the jugs and Z the volume we want to reach to.
The riddle can then be seen as the solution to a Diophantine equation of the form pX + qY = Z.

`p` and `q` indicate how many times a jug needs to be filled (if positive) or emptied (if negative).

The above equation is solvable iff gcd(X, Y) divides Z.

"""
import math

from .exceptions import UnsolvableRiddle
from .game import JugRiddle
from .types import Jug, JugAction


def is_solvable(riddle: JugRiddle) -> bool:
    """Determines if the given riddle is solvable or not.
    For a riddle to be solvable, we ask the goal to be less or equal to capacity of one
    of the jugs.
    If so, we checked whether the necessary and sufficient condition for Diophantine equations
    holds.
    """
    return (riddle.goal <= max(riddle.jug_1_capacity, riddle.jug_2_capacity)) and (
        riddle.goal % math.gcd(riddle.jug_1_capacity, riddle.jug_2_capacity) == 0
    )


def __solve_riddle_by_always_poruing_from_one_jug(
    riddle: JugRiddle, pouring_jug: Jug
) -> None:
    """
    Solves the Water Jug Riddle by repeatedly pouring water from one jug into the other.

    With are assumming the riddle is solvable, hence there exists values for `s` and `t` such that:
         s · Jug1 + t · Jug2 = Goal
    These values represent how many times a jug was filled (if value is positive) or emptied (if value is negative).

    This function applies the specified algorithm to solve the riddle. It takes a `JugRiddle`
    instance and a pouring jug as input and modifies the `JugRiddle` instance to find a solution.

    Args:
        riddle (JugRiddle): An instance of the Water Jug Riddle.
        pouring_jug (Jug): The jug from which water will be poured into the other jug.

    Note:
        The algorithm repeatedly fills the specified jug and transfers its contents to the other
        jug until the desired amount of water is obtained in one of the jugs. Whenever the other jug
        becomes full, it is emptied out to continue the pouring process.
    """
    pour_to_jug = riddle.the_other_jug(pouring_jug)

    # Start by filling the "from" jug
    riddle.take_action(pouring_jug, JugAction.FILL)
    while not riddle.done:
        # Transfer from the pouring jug into the other jug
        riddle.take_action(pouring_jug, JugAction.TRANSFER)

        if riddle.almost_done:
            # We are almost there. We now have the goal in one of our jugs. Empty the other one.
            riddle.finish_almost_done_game()
        else:
            # If pouring jug becomes empty, fill it
            if riddle.jug(pouring_jug) == 0:
                riddle.take_action(pouring_jug, JugAction.FILL)

            # If "other" jug becomes full, empty it
            if riddle.jug(pour_to_jug) == riddle.jug_capacity(pour_to_jug):
                riddle.take_action(pour_to_jug, JugAction.EMPTY)


def solve(riddle: JugRiddle) -> JugRiddle:
    """
    Finds the set of states that will solve the given jug riddle in the most efficient way (i.e. with the minimum
    amount of actions) if any.

    If no solution exists, an exception is raised.
    """
    if not is_solvable(riddle):
        # Riddle is not solvable.
        raise UnsolvableRiddle("Riddle can't be solved!")

    # To find the sequence of operations, the following algorithm is applied:
    #  * Repeat until the desired amount of water is obtained:
    #      – Fill one jug.
    #      – Transfer water into the other jug. Whenever the second jug becomes full, empty it out.
    # In order to know which sequence of actions is optimal (i.e. less number of actions taken), we will consider both
    # possible scenarios:
    #  1-  Always pour from jug 1 into jug 2
    #  2-  Always pour from jug 2 into jug 1
    # and check which reaches the solution in the minimum number of steps

    riddle_1 = JugRiddle(riddle.jug_1_capacity, riddle.jug_2_capacity, riddle.goal)
    __solve_riddle_by_always_poruing_from_one_jug(riddle_1, Jug.JUG_1)
    riddle_2 = JugRiddle(riddle.jug_1_capacity, riddle.jug_2_capacity, riddle.goal)
    __solve_riddle_by_always_poruing_from_one_jug(riddle_2, Jug.JUG_2)

    sol = min(riddle_1, riddle_2, key=len)
    return sol
