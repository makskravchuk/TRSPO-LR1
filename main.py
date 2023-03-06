import sys
import time

import tools
from entities import PointsFactory


def timer(function):
    def wrap_function(*args):
        start = time.time()
        result = function(*args)
        end = time.time()
        execution_time = end - start
        return result, execution_time

    return wrap_function


def commands():
    text = "/exit - вихід\n" \
           "/generate - згенерувати випадкові точки\n" \
           "/input - завантажити точки записані в файл str_data.txt\n" \
           "/download - завантажити раніше збережені випадкові точки\n" \
           "/help - список команд\n"
    print(text)


if __name__ == "__main__":
    commands()
    while True:
        match input(">").replace(">", ""):
            case "/exit":
                sys.exit(0)
            case "/generate":
                number = int(input("Введіть кількість:"))
                points = PointsFactory.generate_points(number)
                while True:
                    answer = input("Зберегти згенеровані дані в файл[y/n]?:")
                    if answer == "y":
                        PointsFactory.safe_points(points)
                    elif answer == "n":
                        break
                break
            case "/input":
                points = PointsFactory.get_file_input_points()
                break
            case "/download":
                points = PointsFactory.load_points()
                break
            case "/help":
                commands()

    #print(f"Задані точки: {points}")

    print("Послідовне виконання:")
    print(f"Результат:")
    results1 = timer(tools.find_gravity_center)(points)
    print(f"Час виконання:{results1[1]}")
    print(f"Результат:{results1[0]}")

    print("Виконання з використанням паралельних обчислень(варіант 1):")
    calculator = tools.GravityCenterCalculator(points)
    results2 = timer(calculator.find_gravity_center)()
    print(f"Час виконання:{results2[1]}")
    print(f"Результат:{results2[0]}")

    print("Виконання з використанням паралельних обчислень(варіант 2):")
    results3 = timer(tools.find_gravity_center_parallel)(points, 3)
    print(f"Час виконання:{results3[1]}")
    print(f"Результат:{results3[0]}")
