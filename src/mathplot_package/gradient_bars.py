import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

bar = ax.bar([1,2,3,4,5,6],[4,5,6,3,7,5])

def gradientbars(bars):
    grad = np.atleast_2d(np.linspace(0,1,256)).T
    ax = bars[0].axes
    lim = ax.get_xlim()+ax.get_ylim()
    for bar in bars:
        bar.set_zorder(1)
        bar.set_facecolor("none")
        x,y = bar.get_xy()
        w, h = bar.get_width(), bar.get_height()
        ax.imshow(grad, extent=[x,x+w,y,y+h], aspect="auto", zorder=0)
    ax.axis(lim)

gradientbars(bar)

plt.show()
