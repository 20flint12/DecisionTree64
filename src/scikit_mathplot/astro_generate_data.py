import math
import random


for i in range(0, 365):

    m = i/12.5
    mf = math.sin(2*3.14*m)*180+180
    taste = random.randint(3, 9)
    food = random.randint(1, 5)

    print(i, ',\t', int(mf), ',\t', taste, ',\t', food)
