import math


class LuasLingkaran:
    def __init__(self, radius):
        self.radius = radius

    def calculate(self):
        return math.pi * self.radius**2
