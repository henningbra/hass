
import unittest
from apps.core.math import MovingAverage


class TestMovingAverage(unittest.TestCase):

    def setUp(self):
        self.items = [1, 1, 0.9, 1.1]
        self.ma = MovingAverage(4)

    def test_full_queue(self):
            for item in self.items:
                result = self.ma.next(item)
            assert result == 1

    def test_overflow_queue(self):
        self.items.append(1)
        for item in self.items:
            result = self.ma.next(item)
        assert result == 1
