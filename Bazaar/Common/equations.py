from pydantic import BaseModel

from Bazaar.Common.equation import Equation
from Bazaar.Common.pebble_collection import PebbleCollection


class EquationTable(BaseModel):
    """
    The EquationTable class represents a table of equations in the game of Bazaar. Each equation table
    holds a list of Equations, representing the equations available to the player.
    """
    equations: list[Equation]

    def __init__(self, equations: list[Equation]) -> None:
        """
        Creates a new instance of the EquationTable class.

        Attributes:
            equations (list[Equation]): All the pebble equations defined.
        """
        super().__init__(equations=equations)

    def get_equations(self) -> list[Equation]:
        return self.equations

    def get_usable(self, pebbles: PebbleCollection) -> list[Equation]:
        """
        Returns all the equations that can be used by the given PebbleCollection (i.e. where all the pebbles
        on at least one side of the equation are fully contained within the given PebbleCollection).

        Parameters:
            pebbles (PebbleCollection): The collection of pebbles to check usability for.

        Returns:
            A list of pebble equations that can be used given the passed in PebbleCollection.
        """
        return [equation for equation in self.equations if equation.is_usable(pebbles)]

    def __str__(self):
        return f"EquationTable({self.get_equations()})"
