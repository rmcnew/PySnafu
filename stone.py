# class for a stone
from coordinate import Coordinate


class Stone(Coordinate):

    def __init__(self, x, y):
        super(Coordinate, self).__init__(x, y)
