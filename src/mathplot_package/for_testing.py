
import matplotlib.pyplot as plt

# create a figure and axes
fig, ax = plt.subplots()

# create a line
x = [1, 2, 3, 4, 5]
y = [1, 2, 3, 2, 1]
line, = ax.plot(x, y)

print(line, line.get_ydata()[3])
# add an annotation with a multi-line text
ax.annotate("Line 1\nLine 2\nLine 3\nytu",
            xy=(3, 2.76),
            # xytext=(3, 1.76),
            )

plt.show()