from tkinter import *


def show(chart, window_dimensions, window_title, frame_color, canvas_margin):
    """Take a chart and create a window representation, using Tkinter."""

    #Make the window
    root = Tk()
    root.title(window_title)
    root.geometry("%ix%i" % (window_dimensions[0], window_dimensions[1]))

    #Make the background
    root.background = Frame(root, background=frame_color, bd=0)
    root.background.pack(fill=BOTH, expand=YES)

    #Make the canvas
    root.background.canvas = ChartCanvas(root.background, chart.canvas,
     background=chart.background_color, highlightthickness=0)
    root.background.canvas.pack(fill=BOTH, expand=YES, padx=canvas_margin, pady=canvas_margin)

    root.mainloop()



class ChartCanvas(Canvas):
    """A tkinter canvas which repaints itself upon resizing. It has a
    QuickPlots canvas telling it what to do."""

    def __init__(self, master, qp_canvas, **kwargs):
        Canvas.__init__(self, master, **kwargs)
        self.qp_canvas = qp_canvas
        self.bind("<Configure>", self.request_repaint)


    def request_repaint(self, event):
        """This method will execute when the canvas is resized."""
        self.qp_canvas.paint_to_tkinter(self)



TKINTER_LINE_STYLES = {
 "." : (1, 2),
 "--": (3, 2)
}

def _line_paint(graphic, tkinter_canvas):
    tkinter_canvas.create_line(
    graphic.start_x, graphic.start_y,
    graphic.end_x, graphic.end_y,
    dash=TKINTER_LINE_STYLES.get(graphic.style),
    fill=graphic.color,
    width=graphic.width
    )


def _rectangle_paint(graphic, tkinter_canvas):
    tkinter_canvas.create_rectangle(
     graphic.x, graphic.y,
     graphic.x + graphic.width, graphic.y + graphic.height,
     width=graphic.line_width,
     dash=TKINTER_LINE_STYLES.get(graphic.line_style),
     outline=graphic.line_color,
     fill=graphic.fill_color
    )


def _text_paint(graphic, tkinter_canvas):
    anchor = None
    if graphic.horizontal_align == "center":
        if graphic.vertical_align == "center":
            anchor = CENTER
        elif graphic.vertical_align == "top":
            anchor = N
        elif graphic.vertical_align == "bottom":
            anchor = S
    elif graphic.horizontal_align == "left":
        if graphic.vertical_align == "center":
            anchor = W
        elif graphic.vertical_align == "top":
            anchor = NW
        elif graphic.vertical_align == "bottom":
            anchor = SW
    elif graphic.horizontal_align == "right":
        if graphic.vertical_align == "center":
            anchor = E
        elif graphic.vertical_align == "top":
            anchor = NE
        elif graphic.vertical_align == "bottom":
            anchor = SE

    tkinter_canvas.create_text(
     graphic.x, graphic.y,
     anchor=anchor,
     text=graphic.text,
     font=(graphic.font, graphic.font_size),
     fill=graphic.color
    )


def _circle_paint(graphic, tkinter):
    tkinter_canvas.create_oval(
     graphic.x - graphic.radius, graphic.y - graphic.radius,
     graphic.x + graphic.radius, graphic.y + graphic.radius,
     width=graphic.line_width,
     dash=TKINTER_LINE_STYLES.get(graphic.line_style),
     outline=graphic.line_color,
     fill=graphic.fill_color
    )


def _arc_paint(graphc, tkinter):
    tkinter_canvas.create_oval(
     graphic.x - graphic.radius, graphic.y - graphic.radius,
     graphic.x + graphic.radius, graphic.y + graphic.radius,
     start=graphic.end - 90 if graphic.clockwise else graphic.start - 90,
     extent=graphic.end - graphic.start,
     style=PIESLICE if graphic.show_radii else ARC,
     width=graphic.line_width,
     dash=TKINTER_LINE_STYLES.get(graphic.line_style),
     outline=graphic.line_color,
     fill=graphic.fill_color
    )
