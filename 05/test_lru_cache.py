from unittest import TestCase
from lru_cache import LRUCache


class TestLRUCache(TestCase):
    def test_simple_set_get(self):
        cache = LRUCache(3)

        cache["k1"] = "val1"
        cache["k2"] = "val2"

        self.assertEqual("val1", cache["k1"])
        self.assertEqual("val2", cache["k2"])
        self.assertEqual(None, cache["k3"])

        cache["k3"] = "val3"
        self.assertEqual("val3", cache["k3"])
        self.assertEqual(None, cache["k4"])

    def test_limit_set_get(self):
        cache = LRUCache(3)

        cache["k1"] = "val1"
        cache["k2"] = "val2"
        cache["k3"] = "val3"

        self.assertEqual("val3", cache["k3"])
        self.assertEqual("val2", cache["k2"])
        self.assertEqual("val1", cache["k1"])
        self.assertEqual(None, cache["k4"])

        cache["k4"] = "new_val"

        self.assertEqual(None, cache["k3"])
        self.assertEqual("val2", cache["k2"])
        self.assertEqual("val1", cache["k1"])
        self.assertEqual("new_val", cache["k4"])
