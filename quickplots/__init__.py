from .data import *
import random
from quickplots import tkdisplay

COLORS = ["#F15854", "#60BD68", "#5DA5DA", "#FAA43A",
 "#F17CB0", "#B2912F", "#B276B2", "#DECF3F", "#4D4D4D"]


class Chart:
    """Something with a window representation and a single canvas"""

    can_grid = False

    def __init__(self, title="", legend=False, window_dimensions=[900, 700],
     window_title="", background_color="#CCCCCC", canvas_margin=50, debug=False):
        self.title = title
        self.legend = legend
        self.window_dimensions = window_dimensions
        self.window_title = window_title
        self.background_color = background_color
        self.canvas_margin = canvas_margin
        self.debug = debug

        self.labels = []


    show = tkdisplay.show
    _prepare_canvas = tkdisplay._chart_prepare_canvas
    _draw_grids = tkdisplay._empty
    _paint_series = tkdisplay._empty
    _draw_plot_bounds = tkdisplay._empty
    _write_title = tkdisplay._chart_write_title
    _create_legend = tkdisplay._chart_create_legend
    _debug_lines = tkdisplay._chart_debug_lines



class PieChart(Chart):
    """A pie chart."""

    def __init__(self, data, colors=None, labels=None, **kwargs):
        Chart.__init__(self, **kwargs)

        self.data = data

        #Assign labels (and make sure there are the right amount)
        if labels is None:
            self.labels = [""] * len(data)
        else:
            assert len(labels) == len(data), "Number of labels does not match data points"
            self.labels = labels

        #Assign colors (and make sure there are the right amount)
        if colors is None:
            if len(data) <= len(COLORS):
                self.colors = COLORS[:len(data)]
            else:
                self.colors = COLORS[:]
                while len(self.colors) != len(data):
                    self.colors.append(generate_random_color())
        else:
            assert len(colors) == len(data), "Number of colors does not match data points"
            self.colors = colors


    _prepare_canvas = tkdisplay._pie_prepare_canvas
    _paint_series = tkdisplay._pie_paint_series
    _create_legend = tkdisplay._pie_create_legend
    _debug_lines = tkdisplay._pie_debug_lines



class AxisChart(Chart):
    """A chart with axes"""

    can_grid = True

    def __init__(self, x_limit=[0,1], x_ticks=None, x_tick_labels=None, x_label="",
     y_limit=[0,1], y_ticks=None, y_tick_labels=None, y_label="", grid=True, **kwargs):
        Chart.__init__(self, **kwargs)

        self.x_limit = check_series_for_dates(x_limit)
        self.x_ticks = self.x_limit if x_ticks is None else check_series_for_dates(x_ticks)
        if x_tick_labels is None:
            self.x_tick_labels = [str(t) for t in self.x_ticks]
        else:
            self.x_tick_labels = x_tick_labels
        self.x_label = x_label

        self.y_limit = y_limit
        self.y_ticks = y_limit if y_ticks is None else y_ticks
        if y_tick_labels is None:
            self.y_tick_labels = [str(t) for t in self.y_ticks]
        else:
            self.y_tick_labels = y_tick_labels
        self.y_label = y_label

        self.grid = grid


    _prepare_canvas = tkdisplay._axis_prepare_canvas
    _draw_grids = tkdisplay._axis_draw_grids
    _draw_plot_bounds = tkdisplay._axis_draw_plot_bounds
    _debug_lines = tkdisplay._axis_debug_lines
