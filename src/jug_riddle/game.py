import logging
from dataclasses import dataclass
from typing import Final

from .types import Jug, JugAction
from .exceptions import InvalidAction

LOG = logging.getLogger(__name__)


@dataclass
class JugRiddleState:
    """
    This class represents how many gallons each jug of the Jug Riddle has.
    It is used to represent the state of the riddle at any given point.
    """

    jug_1: int
    jug_2: int

    @property
    def total_water(self):
        """Calculate the total amount of water in both jugs."""
        return self.jug_1 + self.jug_2

    def __str__(self):
        return (
            f"Jug 1: {self.jug_1} | Jug 2: {self.jug_2} || (Total: {self.total_water})"
        )


class JugRiddle:
    """
    Represents an instance of the Water Jug Riddle, a classic mathematical puzzle.

    The Water Jug Riddle involves two jugs with different capacities (Jug 1 and Jug 2) and
    a goal of measuring a specific amount of water. This class provides methods to simulate
    and try to solve the riddle.

    Args:
        jug_1 (int): Capacity of Jug 1 in liters.
        jug_2 (int): Capacity of Jug 2 in liters.
        goal (int): The target amount of water in liters to achieve.

    Attributes:
        jug_1_capacity (int): Capacity of Jug 1.
        jug_2_capacity (int): Capacity of Jug 2.
        goal (int): The target amount of water to achieve.
        _states (list[JugRiddleState]): List of riddle states during the simulation.
        _actions (list[tuple[JugAction, Jug]]): List of actions taken during the simulation.

    Note:
        This class assumes that both jug capacities (jug_1 and jug_2) are positive integers,
        and the goal is a non-negative integer.
    """


    def __init__(self, jug_1: int, jug_2: int, goal: int):
        """
        Initialize the JugRiddle instance with jug capacities and a goal.

        Args:
            jug_1 (int): Capacity of Jug 1.
            jug_2 (int): Capacity of Jug 2.
            goal (int): The target amount of water to achieve.
        """
        self.jug_1_capacity: Final = jug_1
        self.jug_2_capacity: Final = jug_2
        self.goal: Final = goal
        self._states = [JugRiddleState(0, 0)]
        self._actions = []

    def __str__(self):
        return (
            f"Jug1: {self.state.jug_1}/{self.jug_1_capacity} | "
            f"Jug2: {self.state.jug_2}/{self.jug_2_capacity} || "
            f"(Total: {self.state.total_water})"
        )

    def __len__(self):
        """We call the number of actions taken so far in a riddle, the length of it"""
        return len(self._actions)

    @property
    def state(self) -> JugRiddleState:
        """Property representing the current state of the riddle"""
        return self._states[-1]

    @property
    def done(self) -> bool:
        """Checks whether the riddle has been solved or not.
        We assume the goal has been reached when the target gallons are reached while
        adding up the gallons on each jug.
        """
        return self.state.total_water == self.goal

    @property
    def almost_done(self) -> bool:
        """
        Checks if (at least) one of the jugs has the target water quantity.
        """
        return self.jug(Jug.JUG_1) == self.goal or self.jug(Jug.JUG_2) == self.goal

    def finish_almost_done_game(self):
        """
        When we are almost done (see `almoast_done` property), we take the
        required "EMPTY" action (if any) to actually reach the goal.
        """
        if not self.almost_done:
            raise InvalidAction("Game is not almost done!")
        if self.state.total_water != self.goal:
            if self.jug(Jug.JUG_1) == self.goal:
                self.take_action(Jug.JUG_2, JugAction.EMPTY)
            else:
                self.take_action(Jug.JUG_1, JugAction.EMPTY)

    def jug(self, jug: Jug) -> int:
        """Returns the gallons of a jug (Jug 1 | Jug 2) at any given point"""
        if jug == Jug.JUG_1:
            return self.state.jug_1
        return self.state.jug_2

    def jug_capacity(self, jug: Jug) -> int:
        """Returns the capacity (i.e. gallons it can potentially hold) of a jug (Jug 1 | Jug 2) for the given riidle"""
        if jug == Jug.JUG_1:
            return self.jug_1_capacity
        return self.jug_2_capacity

    def jug_remaining_capacity(self, jug: Jug) -> int:
        """Returns the free space (i.e. gallons it can currently hold) of a jug (Jug 1 | Jug 2) at any given point"""
        return self.jug_capacity(jug) - self.jug(jug)

    def __transition_to_state(self, jug_1: int, jug_2: int):
        """Moves the riddle to a new state where Jug 1 contains `jug_1` gallons and Jug 2 contains `jug_2` gallons.
        No validation is performed, we just assume the given values are valid"""
        self._states.append(JugRiddleState(jug_1, jug_2))

    @classmethod
    def the_other_jug(cls, jug: Jug):
        """Given a jug, returns the ohter jug on a riddle"""
        if jug == Jug.JUG_1:
            return Jug.JUG_2
        return Jug.JUG_1

    def take_action(self, jug: Jug, jug_action: JugAction):
        """
        This method takes a Jug and an action and updates the state of the riddle accordingly.
        If the action is not valid, an InvalidAction exception is raised.
        """
        if jug_action == JugAction.EMPTY and self.jug(jug) == 0:
            LOG.error("Trying to empty jug %d which is already empty!", jug.value)
            raise InvalidAction("Trying to empty an already empty jug!")

        if jug_action == JugAction.FILL and self.jug(jug) == self.jug_capacity(jug):
            LOG.error("Trying to fill jug %d which is already full!", jug.value)
            raise InvalidAction("Trying to fill an already full jug!")

        after_action_jugs = {
            Jug.JUG_1: self.jug(jug.JUG_1),
            Jug.JUG_2: self.jug(jug.JUG_2),
        }

        if jug_action == JugAction.FILL:
            after_action_jugs[jug] = self.jug_capacity(jug)
        elif jug_action == JugAction.EMPTY:
            after_action_jugs[jug] = 0
        elif jug_action == JugAction.TRANSFER:
            transfer_from = jug
            transfer_to = self.the_other_jug(jug)
            if self.jug(transfer_from) == 0:
                LOG.error(
                    "Transferring from jar %d which is empty!", transfer_from.value
                )
                raise InvalidAction("Transferring from empty jar!")
            if self.jug(transfer_to) == self.jug_capacity(transfer_to):
                LOG.error("Transferring to jar %d which is full!", transfer_to.value)
                raise InvalidAction("Transferring to full jar!")
            water_to_transfer = min(
                self.jug_remaining_capacity(transfer_to), self.jug(transfer_from)
            )
            after_action_jugs[transfer_to] += water_to_transfer
            after_action_jugs[transfer_from] -= water_to_transfer
        self._actions.append((jug_action, jug))
        self.__transition_to_state(
            after_action_jugs[Jug.JUG_1], after_action_jugs[Jug.JUG_2]
        )

    def view_solution(self) -> str:
        """Returns a string that shows the solution (if already found) of the riddle"""
        if not self.done:
            return "Riddle is not yet solved!"
        return "\n".join(
            [
                f"Step {idx+1}: {action.name} JUG {jug.value}"
                for idx, (action, jug) in enumerate(self._actions)
            ]
        )
