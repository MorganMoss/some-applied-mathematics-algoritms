import math

from graphs import *


def main():
    global f, x_ls

    x_ls = [0, 0.25, 0.5, 0.75]
    f = lambda x : math.e**-x

    initialize()
    modify(sc = 200,ask=False)

    plot(f, x_ls, (255,255,255), 20)

    show()


def natural_cubic_spline(approx_x):
    ...





if __name__ == '__main__': 
    main()