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
        '''self.chart._paint_grids()
        self.chart._paint_series()
        self.chart._paint_plot_bounds()
        self.chart._write_title()
        self.chart._write_legend_labels()
        self.chart._paint_legend_symbols()
        self.chart._paint_debug_lines()'''


    def draw_to_tkinter(self, tkinter_canvas):
        pass
