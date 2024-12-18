import unittest
from pydantic import ValidationError
from Bazaar.Common.pebble_collection import PebbleCollection, Color
from Bazaar.Common.equations import Equation, EquationTable
from pygame import Surface
from Bazaar.Common.pygame_rendering import equation_to_image, equation_table_to_image
import pygame

pygame.init()


class TestEquation(unittest.TestCase):

    def test_valid_initialization(self):
        left = PebbleCollection({Color.RED: 2, Color.BLUE: 1})
        right = PebbleCollection({Color.GREEN: 2, Color.YELLOW: 1})
        equation = Equation(left=left, right=right)
        self.assertEqual(equation.left, left)
        self.assertEqual(equation.right, right)

    def test_is_usable_true(self):
        equation = Equation(
            left=PebbleCollection({Color.RED: 2, Color.BLUE: 1}),
            right=PebbleCollection({Color.GREEN: 2, Color.YELLOW: 1}),
        )
        pebbles = PebbleCollection({Color.RED: 3, Color.BLUE: 1, Color.GREEN: 1})
        self.assertTrue(equation.is_usable(pebbles))

    def test_is_usable_false(self):
        equation = Equation(
            left=PebbleCollection({Color.RED: 2, Color.BLUE: 1}),
            right=PebbleCollection({Color.GREEN: 2, Color.YELLOW: 1}),
        )
        pebbles = PebbleCollection({Color.RED: 1, Color.BLUE: 1})
        self.assertFalse(equation.is_usable(pebbles))

    def test_to_image(self):
        equation = Equation(
            left=PebbleCollection({Color.RED: 2, Color.BLUE: 1}),
            right=PebbleCollection({Color.GREEN: 2, Color.YELLOW: 1}),
        )
        image = equation_to_image(equation, 100)
        self.assertIsInstance(image, Surface)
        self.assertEqual(image.get_size(), (900, 100))


class TestEquationTable(unittest.TestCase):

    def test_valid_initialization(self):
        eq1 = Equation(
            left=PebbleCollection({Color.RED: 2}),
            right=PebbleCollection({Color.BLUE: 1}),
        )
        eq2 = Equation(
            left=PebbleCollection({Color.GREEN: 1}),
            right=PebbleCollection({Color.YELLOW: 2}),
        )
        table = EquationTable(equations=[eq1, eq2])
        self.assertEqual(len(table._equations), 2)

    def test_invalid_initialization_empty_left(self):
        with self.assertRaises(ValidationError):
            Equation(
                left=PebbleCollection({}),
                right=PebbleCollection({Color.GREEN: 2, Color.YELLOW: 1}),
            )

    def test_invalid_initialization_empty_right(self):
        with self.assertRaises(ValidationError):
            Equation(
                left=PebbleCollection({Color.GREEN: 2, Color.YELLOW: 1}),
                right=PebbleCollection({}),
            )

    def test_invalid_initialization_same_color(self):
        with self.assertRaises(ValidationError):
            Equation(
                left=PebbleCollection({Color.RED: 1, Color.BLUE: 1}),
                right=PebbleCollection({Color.RED: 2, Color.YELLOW: 1}),
            )

    def test_get_usable(self):
        eq1 = Equation(
            left=PebbleCollection({Color.RED: 2}),
            right=PebbleCollection({Color.BLUE: 1}),
        )
        eq2 = Equation(
            left=PebbleCollection({Color.GREEN: 1}),
            right=PebbleCollection({Color.YELLOW: 2}),
        )
        table = EquationTable(equations=[eq1, eq2])
        pebbles = PebbleCollection({Color.RED: 2, Color.GREEN: 1})
        usable = table.get_usable(pebbles)
        self.assertEqual(len(usable), 2)

    def test_get_usable_empty(self):
        eq1 = Equation(
            left=PebbleCollection({Color.RED: 2}),
            right=PebbleCollection({Color.BLUE: 1}),
        )
        eq2 = Equation(
            left=PebbleCollection({Color.GREEN: 1}),
            right=PebbleCollection({Color.YELLOW: 2}),
        )
        table = EquationTable(equations=[eq1, eq2])
        pebbles = PebbleCollection({Color.WHITE: 1})
        usable = table.get_usable(pebbles)
        self.assertEqual(len(usable), 0)

    def test_to_image(self):
        eq1 = Equation(
            left=PebbleCollection({Color.RED: 2}),
            right=PebbleCollection({Color.BLUE: 1}),
        )
        eq2 = Equation(
            left=PebbleCollection({Color.GREEN: 1}),
            right=PebbleCollection({Color.YELLOW: 2}),
        )
        table = EquationTable(equations=[eq1, eq2])
        image = equation_table_to_image(table, 900, 200)
        self.assertIsInstance(image, Surface)
        self.assertEqual(image.get_size(), (900, 200))


if __name__ == "__main__":
    unittest.main()
