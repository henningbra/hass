from collections import deque

class MovingAverage(object):
    """
    Credits: https://high-python-ext-3-algorithms.readthedocs.io/ko/latest/chapter16.html#moving-average
    
    """
    def __init__(self, size):
        """
        Initialize your data structure here.
        :type size: int
        """
        self.queue = deque(maxlen=size)

    def next(self, val):
        """
        :type val: int
        :rtype: float
        """
        self.queue.append(val)
        return sum(self.queue) / len(self.queue)
