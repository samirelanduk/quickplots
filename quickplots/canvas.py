from . import tkdisplay
from . import svgdisplay
from . import textsize

class QuickplotsCanvas:
    """A generic canvas, associated with a chart."""

    def __init__(self, chart):
        self.chart = chart
        self.width = 1
        self.height = 1
        self.graphics = []


    def __repr__(self):
        return "<QuickplotsCanvas(%i graphics objects)>" % len(self.graphics)


    def request_repaint(self, width, height):
        self.width = width
        self.height = height

        self.chart._paint_to_canvas()


    def create_text(self, *args, **kwargs):
        self.graphics.append(TextGraphic(*args, **kwargs))


    def create_line(self, *args, **kwargs):
        self.graphics.append(LineGraphic(*args, **kwargs))


    def create_rectangle(self, *args, **kwargs):
        self.graphics.append(RectangleGraphic(*args, **kwargs))


    def paint_to_tkinter(self, tkinter_canvas):
        tkinter_canvas.delete("all")
        width = tkinter_canvas.winfo_width()
        height = tkinter_canvas.winfo_height()
        self.request_repaint(width, height)
        for graphic in self.graphics:
            graphic.paint_to_tkinter(tkinter_canvas)


class LineGraphic:

    def __init__(self, start_x, start_y, end_x, end_y, width=1, style="-", color="#000000"):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.width = width
        self.style = style
        self.color = color


    def __repr__(self):
        return "Line from (%i, %i) to (%i, %i)" % (
         self.start_x,
         self.start_y,
         self.end_x,
         self.end_y
        )


    paint_to_tkinter = tkdisplay._line_paint
    to_svg = svgdisplay._line_paint



class GenericRectangle:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


    def __repr__(self):
        return "(%i, %i) %i × %i" % (
         self.x,
         self.y,
         self.width,
         self.height
        )



class TextGraphic:

    def __init__(self, x, y, horizontal_align="center", vertical_align="center",
     text="", font="Tahoma", font_size=24, color="#000000"):
        self.x = x
        self.y = y
        self.horizontal_align = horizontal_align
        self.vertical_align = vertical_align
        self.text = text
        self.font = font
        self.font_size = font_size if isinstance(
         font_size, int) else textsize.get_font_size(
          text, font_size[0], font_size[1])
        self.color = color


    def __repr__(self):
        return '"%s" - (%i, %i)' % (self.text, self.x, self.y)


    paint_to_tkinter = tkdisplay._text_paint
    to_svg = svgdisplay._text_paint



class RectangleGraphic(GenericRectangle):

    def __init__(self, *args, line_width=1, line_style="-", line_color="#000000", fill_color=None, **kwargs):
        GenericRectangle.__init__(self, *args, **kwargs)
        self.line_width = line_width
        self.line_style = line_style
        self.line_color = line_color
        self.fill_color = fill_color


    def __repr__(self):
        return 'Rectangle - %s' % GenericRectangle.__repr__(self)


    paint_to_tkinter = tkdisplay._rectangle_paint
    to_svg = svgdisplay._rectangle_paint



class CircleGraphic:

    def __init__(self, x, y, radius, line_width=1, line_style="-", line_color="#000000", fill_color=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.line_width = line_width
        self.line_style = line_style
        self.line_color = line_color
        self.fill_color = fill_color


    def __repr__(self):
        return 'Cicle - (%i, %i)' % (self.x, self.y)
