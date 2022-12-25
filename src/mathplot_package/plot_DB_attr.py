import matplotlib.pyplot as plt
import numpy as np


def plot_list(value_list, file_name="user_photo.png"):

    plt.xlabel('x-axis label')
    plt.ylabel('y-axis label')
    plt.title('Matplotlib Example')
    # print(value_list)
    y_points = np.array(value_list)
    plt.plot(y_points)
    # plt.show()

    res = plt.savefig(file_name)
    print(res)


if __name__ == '__main__':
    values = [79, 79, 79, 79, 79, 82, 82, 82, 82, 82, 82, 82, 82, 82, 82, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79,
              79, 79, 79, 79, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 76, 76, 76, 76, 76, 76, 76, 76, 76, 76,
              76, 76, 76, 76, 76, 76, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80,
              80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 84, 84, 84, 84,
              84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 87, 87,
              87, 87, 87]

    plot_list(values, "user_photo2.png")
