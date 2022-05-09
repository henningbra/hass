from collections import deque

class MovingAverage:
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
        :rtype: None
        """
        self.queue.append(val)

    def average(self):
        """
        :type val: int
        :rtype: float
        """
        return round(sum(self.queue) / len(self.queue))
         
