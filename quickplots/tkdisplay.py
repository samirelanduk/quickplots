from tkinter import *


def show(chart, window_dimensions, window_title):
    root = Tk()
    root.title(window_title)
    root.geometry("%ix%i" % (window_dimensions[0], window_dimensions[1]))

    root.mainloop()
