import unittest
from pydantic import ValidationError
from Bazaar.Common.pebble_collection import PebbleCollection, Color
from pygame import Surface
from Bazaar.Common.cards import Card
from Bazaar.Common.pygame_rendering import card_to_image


class TestCard(unittest.TestCase):

    def test_valid_initialization(self):
        cost = PebbleCollection({Color.RED: 2, Color.GREEN: 2, Color.BLUE: 1})
        card = Card(cost=cost, face=True)
        self.assertEqual(card.cost, cost)
        self.assertTrue(card.face)

    def test_invalid_initialization(self):
        invalid_cost = PebbleCollection({Color.RED: 2, Color.GREEN: 2, Color.BLUE: 2})
        with self.assertRaises(ValidationError):
            Card(cost=invalid_cost, face=False)

    def test_can_acquire_true(self):
        cost = PebbleCollection({Color.RED: 2, Color.GREEN: 2, Color.BLUE: 1})
        card = Card(cost=cost, face=True)
        pebbles = PebbleCollection({Color.RED: 3, Color.GREEN: 2, Color.BLUE: 1})
        self.assertTrue(card.can_acquire(pebbles))

    def test_can_acquire_false(self):
        cost = PebbleCollection({Color.RED: 2, Color.GREEN: 2, Color.BLUE: 1})
        card = Card(cost=cost, face=True)
        pebbles = PebbleCollection({Color.RED: 1, Color.GREEN: 2, Color.BLUE: 1})
        self.assertFalse(card.can_acquire(pebbles))

    def test_to_image(self):
        cost = PebbleCollection({Color.RED: 2, Color.GREEN: 2, Color.BLUE: 1})
        card = Card(cost=cost, face=True)
        image = card_to_image(card, 60, 100)
        self.assertIsInstance(image, Surface)
        self.assertEqual(image.get_size(), (60, 100))


if __name__ == "__main__":
    unittest.main()
