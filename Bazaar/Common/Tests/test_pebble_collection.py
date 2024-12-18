import unittest
from pydantic import ValidationError
from Bazaar.Common.pebble_collection import PebbleCollection, Color


class TestPebbleCollection(unittest.TestCase):

    def test_valid_initialization(self):
        pebbles = {Color.RED: 2, Color.BLUE: 3, Color.GREEN: 1}
        collection = PebbleCollection(pebbles=pebbles)
        self.assertEqual(collection.pebbles, pebbles)

    def test_invalid_initialization(self):
        with self.assertRaises(ValidationError):
            PebbleCollection(pebbles={Color.RED: -1})

    def test_getitem(self):
        collection = PebbleCollection(pebbles={Color.RED: 2, Color.BLUE: 3})
        self.assertEqual(collection[Color.RED], 2)
        self.assertEqual(collection[Color.BLUE], 3)
        self.assertEqual(collection[Color.GREEN], 0)

    def test_setitem(self):
        collection = PebbleCollection(pebbles={})
        collection[Color.RED] = 5
        self.assertEqual(collection[Color.RED], 5)
        collection[Color.RED] = 0
        self.assertEqual(collection[Color.RED], 0)

    def test_add(self):
        collection1 = PebbleCollection(pebbles={Color.RED: 2, Color.BLUE: 3})
        collection2 = PebbleCollection(pebbles={Color.RED: 1, Color.GREEN: 2})
        result = collection1 + collection2
        self.assertEqual(result[Color.RED], 3)
        self.assertEqual(result[Color.BLUE], 3)
        self.assertEqual(result[Color.GREEN], 2)

    def test_sub(self):
        collection1 = PebbleCollection(pebbles={Color.RED: 5, Color.BLUE: 3})
        collection2 = PebbleCollection(pebbles={Color.RED: 2, Color.BLUE: 1})
        result = collection1 - collection2
        self.assertEqual(result[Color.RED], 3)
        self.assertEqual(result[Color.BLUE], 2)

    def test_sub_raises_value_error(self):
        collection1 = PebbleCollection(pebbles={Color.RED: 1})
        collection2 = PebbleCollection(pebbles={Color.RED: 2})
        with self.assertRaises(ValueError):
            collection1 - collection2

    def test_ge(self):
        collection1 = PebbleCollection(pebbles={Color.RED: 5, Color.BLUE: 3})
        collection2 = PebbleCollection(pebbles={Color.RED: 5, Color.BLUE: 2})
        self.assertTrue(collection1 >= collection2)
        self.assertFalse(collection2 >= collection1)

    def test_gt(self):
        collection1 = PebbleCollection(pebbles={Color.RED: 5, Color.BLUE: 3})
        collection2 = PebbleCollection(pebbles={Color.RED: 4, Color.BLUE: 2})
        self.assertTrue(collection1 > collection2)
        self.assertFalse(collection2 > collection1)

    def test_le(self):
        collection1 = PebbleCollection(pebbles={Color.RED: 5, Color.BLUE: 3})
        collection2 = PebbleCollection(pebbles={Color.RED: 5, Color.BLUE: 4})
        self.assertTrue(collection1 <= collection2)
        self.assertFalse(collection2 <= collection1)

    def test_lt(self):
        collection1 = PebbleCollection(pebbles={Color.RED: 4, Color.BLUE: 2})
        collection2 = PebbleCollection(pebbles={Color.RED: 5, Color.BLUE: 3})
        self.assertTrue(collection1 < collection2)
        self.assertFalse(collection2 < collection1)

    def test_values(self):
        collection = PebbleCollection(
            pebbles={Color.RED: 2, Color.BLUE: 3, Color.GREEN: 1}
        )
        self.assertEqual(collection.values(), [2, 3, 1])


if __name__ == "__main__":
    unittest.main()
