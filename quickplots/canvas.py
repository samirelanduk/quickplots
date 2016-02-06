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

        self.chart._prepare_canvas()
        self.chart._paint_grids()
        self.chart._paint_series()
        self.chart._paint_plot_bounds()
        self.chart._write_title()
        self.chart._write_legend_labels()
        self.chart._paint_legend_symbols()
        self.chart._paint_debug_lines()


    def create_text(self, *args, **kwargs):
        self.graphics.append(TextGraphic(*args, **kwargs))


    def create_line(self, *args, **kwargs):
        self.graphics.append(LineGraphic(*args, **kwargs))


    def create_rectangle(self, *args, **kwargs):
        self.graphics.append(RectangleGraphic(*args, **kwargs))


    def draw_to_tkinter(self, tkinter_canvas):
        pass


class LineGraphic:

    def __init__(self, start_x, start_y, end_x, end_y, width=1, style="-"):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.width = width
        self.style = style


    def __repr__(self):
        return "Line from (%i, %i) to (%i, %i)" % (
         self.start_x,
         self.start_y,
         self.end_x,
         self.end_y
        )



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



class TextGraphic(GenericRectangle):

    def __init__(self, *args, text="", max_font_size=100, **kwargs):
        GenericRectangle.__init__(self, *args, **kwargs)
        self.text = text
        self.max_font_size = max_font_size


    def __repr__(self):
        return '"%s" - %s' % (self.text, GenericRectangle.__repr__(self))



class RectangleGraphic(GenericRectangle):

    def __init__(self, *args, line_width=1, line_style="-", **kwargs):
        GenericRectangle.__init__(self, *args, **kwargs)
        self.line_width = line_width
        self.line_style = line_style


    def __repr__(self):
        return 'Rectangle - %s' % GenericRectangle.__repr__(self)
