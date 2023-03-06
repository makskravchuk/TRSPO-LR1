import threading

from entities import Point


def calculate_weights_sum(points):
    return sum(point.weight for point in points)


def calculate_sum_of_product(points, axis="x"):
    if axis == "x":
        return sum(point.x_weighted() for point in points)
    elif axis == "y":
        return sum(point.y_weighted() for point in points)


# Послідовне виконання
def find_gravity_center(points):
    weights_sum = calculate_weights_sum(points)
    sum_of_product_x = calculate_sum_of_product(points, "x")
    sum_of_product_y = calculate_sum_of_product(points, "y")
    xc = sum_of_product_x / weights_sum
    yc = sum_of_product_y / weights_sum
    return xc, yc


# Розпаралелювання, варіант 1
class GravityCenterCalculator:

    def __init__(self, points):
        self.__points = points
        self.__x_sum = 0
        self.__y_sum = 0
        self.__total_weight = 0

    def weights_sum(self):
        self.__total_weight = calculate_weights_sum(self.__points)

    def sum_of_product(self, axis="x"):
        if axis == "x":
            self.__x_sum = calculate_sum_of_product(self.__points, axis)
        elif axis == "y":
            self.__y_sum = calculate_sum_of_product(self.__points, axis)

    def find_gravity_center(self):
        thread_total_sum = threading.Thread(target=self.weights_sum)
        thread_x_sum = threading.Thread(target=self.sum_of_product, args=("x",))
        thread_y_sum = threading.Thread(target=self.sum_of_product, args=("y",))

        # запуск потоків
        thread_total_sum.start()
        thread_x_sum.start()
        thread_y_sum.start()

        # очікування завершення потоків
        thread_total_sum.join()
        thread_x_sum.join()
        thread_y_sum.join()

        xc = self.__x_sum / self.__total_weight
        yc = self.__y_sum / self.__total_weight

        return xc, yc


# Розпаралелювання, варіант 2

def process_points(points):
    total_weight = calculate_weights_sum(points)
    xc, yc = find_gravity_center(points)
    return Point(xc, yc, total_weight)


def find_gravity_center_parallel(points, threads_number):
    chunk_size = len(points) // threads_number
    new_centers = []
    threads = []
    for i in range(threads_number):
        start = i * chunk_size
        finish = start + chunk_size if i < threads_number - 1 else len(points)
        chunk = points[start:finish]
        thread = threading.Thread(target=lambda: new_centers.append(process_points(chunk)))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return find_gravity_center(new_centers)
