import random
import pickle


class Point:
    def __init__(self, x=0, y=0, weight=1):
        self._x = x
        self._y = y
        self._weight = weight

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def weight(self):
        return self._weight

    def x_weighted(self):
        return self.x * self.weight

    def y_weighted(self):
        return self.y * self.weight

    def __str__(self):
        return f"(x={self.x},y={self.y},weight={self.weight})"

    def __repr__(self):
        return f"Point(x={self.x},y={self.y},weight={self.weight})"


class PointsFactory:
    file_path = "data.pkl"
    input_data_path = "str_data.txt"

    @staticmethod
    def generate_points(number):
        points = []
        for i in range(number):
            x = random.randrange(0, 1000)
            y = random.randrange(0, 1000)
            weight = random.randrange(1, 500)
            points.append(Point(x, y, weight))
        return points

    @classmethod
    def safe_points(cls, points):
        with open(cls.file_path, "wb") as file:
            pickle.dump(points, file)

    @classmethod
    def load_points(cls):
        with open(cls.file_path, "rb") as file:
            points = pickle.load(file)
        return points

    @classmethod
    def get_file_input_points(cls):
        # format: 4, 5.1, 12
        points = []
        with open(cls.input_data_path, "r") as input_data:
            lines = input_data.readlines()
        for line in lines:
            line = line.strip()
            point_data = line.split(", ")
            point_data = [int(elem) if elem.isdigit() else float(elem) for elem in point_data]
            points.append(Point(point_data[0], point_data[1], point_data[2]))
        return points
