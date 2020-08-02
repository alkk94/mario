class Position(object):
    def __init__(self, point):
        self.x = point[0]
        self.y = point[1]

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_position(self):
        return self.x, self.y

    def change_position(self, x, y):
        self.x += x
        self.y += y

    def scale_position(self, scalar):
        self.x //= scalar
        self.y //= scalar

    def is_same_positions(self, point):
        return self.x == point[0] and self.y == point[1]
