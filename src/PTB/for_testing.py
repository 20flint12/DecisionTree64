
from enum import IntEnum


class Color(IntEnum):
    RED = 1
    GREEN = 2
    BLUE = 3

color = Color.RED

integer = int(color)
print(integer)  # Output: 1


color = Color.RED
string = str(color)
print(string, color, type(color))  # Output: 'Color.RED'


enum_value = Color.RED
int_value = Color.RED + 1
str_value = str(int_value)
print(Color(int_value), str_value)     # "1"

