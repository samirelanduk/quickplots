from .data import *
from . import tkdisplay
import math
import random


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
    _write_legend_labels = tkdisplay._chart_write_legend_labels
    _draw_legend_symbols = tkdisplay._empty
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

        self.x_limit = DataSequence(x_limit)
        self.x_ticks = DataSequence(self.x_limit[:]) if x_ticks is None else DataSequence(x_ticks)
        if x_tick_labels is None:
            self.x_tick_labels = [str(t) for t in self.x_ticks]
        else:
            self.x_tick_labels = x_tick_labels
        self.x_label = x_label

        self.y_limit = y_limit
        self.y_ticks = self.get_y_ticks() if y_ticks is None else y_ticks
        if y_tick_labels is None:
            self.y_tick_labels = [str(t) for t in self.y_ticks]
        else:
            self.y_tick_labels = y_tick_labels
        self.y_label = y_label

        self.grid = grid


    def update_x_tick_labels(self):
        """Reset all x tick labels to be str of x ticks"""
        self.x_tick_labels = [str(t) for t in self.x_ticks]


    def update_y_tick_labels(self):
        """Reset all y tick labels to be str of y ticks"""
        self.y_tick_labels = [str(t) for t in self.y_ticks]


    def get_y_ticks(self):
        difference = self.y_limit[1] - self.y_limit[0]
        l = math.floor(math.log(difference, 10))
        tick = 10 ** l
        neg = math.floor(self.y_limit[0] / tick) * tick
        ticks = [neg + tick]
        while ticks[-1] + tick <= self.y_limit[1]:
            ticks.append(ticks[-1] + tick)
        if self.y_limit[0] not in ticks:
            ticks.append(self.y_limit[0])
        if self.y_limit[1] not in ticks:
            ticks.append(self.y_limit[1])
        return sorted(ticks)



    _prepare_canvas = tkdisplay._axis_prepare_canvas
    _draw_grids = tkdisplay._axis_draw_grids
    _draw_plot_bounds = tkdisplay._axis_draw_plot_bounds
    _debug_lines = tkdisplay._axis_debug_lines



class SingleSeriesAxisChart(AxisChart):
    """An axis chart with a single series on it."""

    def __init__(self, series, series_name="", y_limit_zero=True, **kwargs):
        if "x_limit" not in kwargs or kwargs["x_limit"] is None:
            kwargs["x_limit"] = [min(list(zip(*series))[0]), max(list(zip(*series))[0])]
        if "y_limit" not in kwargs or kwargs["y_limit"] is None:
            kwargs["y_limit"] = [0 if y_limit_zero else min(list(zip(*series))[1]), get_limit(max(list(zip(*series))[1]))]
        AxisChart.__init__(self, **kwargs)

        self.series = Series(series)
        self.series_name = series_name
        self.labels = [self.series_name]


    def generate_moving_average(self, n, keep_axis_limits=False):
        xs, ys = list(zip(*self.series))
        new_y = [sum(ys[i-(n-1):i+1]) / n for i,_ in enumerate(ys[n-1:], start=n-1)]
        new_x = xs[n-1:]
        series = list(zip(new_x, new_y))
        kwargs = {
         "series_name": self.series_name + " moving average",
         "x_label": self.x_label,
         "y_label": self.y_label,
         "legend": self.legend
        }
        if keep_axis_limits:
            kwargs["x_limit"] = self.x_limit
            kwargs["y_limit"] = self.y_limit
            kwargs["x_ticks"] = self.x_ticks
            kwargs["x_tick_labels"] = self.x_tick_labels
            kwargs["y_ticks"] = self.y_ticks
            kwargs["y_tick_labels"] = self.y_tick_labels
        return LineChart(series, color="#000000", **kwargs)



class LineChart(SingleSeriesAxisChart):
    """A line chart."""

    def __init__(self, *args, color=None, width=2, style="-", **kwargs):
        SingleSeriesAxisChart.__init__(self, *args, **kwargs)
        if color is None:
            self.color = random.choice(COLORS)
        else:
            self.color = color
        self.width = width
        self.style = style


    _paint_series = tkdisplay._line_paint_series
    _draw_legend_symbols = tkdisplay._line_draw_legend_symbols



class BarChart(SingleSeriesAxisChart):
    """A bar chart"""

    def __init__(self, *args, color=None, bar_width=1, align="center", edge_width=1, edge_color="#000000", **kwargs):
        SingleSeriesAxisChart.__init__(self, *args, **kwargs)

        if color is None:
            self.color = random.choice(COLORS)
        else:
            self.color = color

        self.bar_width = bar_width
        self.align = align
        self.edge_width = edge_width
        self.edge_color = edge_color


    _paint_series = tkdisplay._bar_paint_series
    _draw_legend_symbols = tkdisplay._bar_draw_legend_symbols



class ScatterChart(SingleSeriesAxisChart):
    """A scatter chart."""

    def __init__(self, *args, color=None, marker="x", size=10, edge_width=1, edge_color="#000000", **kwargs):
        SingleSeriesAxisChart.__init__(self, *args, **kwargs)

        if color is None:
            self.color = random.choice(COLORS)
        else:
            self.color = color
        self.marker = marker
        self.size = size
        self.edge_width = edge_width
        self.edge_color = edge_color



    _paint_series = tkdisplay._scatter_paint_series
    _draw_legend_symbols = tkdisplay._scatter_draw_legend_symbols

class MultiSeriesAxisChart(AxisChart):
    """An axis chart with multiple series on it."""

    def __init__(self, charts, **kwargs):
        if "x_limit" not in kwargs or kwargs["x_limit"] is None:
            kwargs["x_limit"] = [min([chart.x_limit[0] for chart in charts]),
            max([chart.x_limit[1] for chart in charts])]
        if "y_limit" not in kwargs or kwargs["y_limit"] is None:
            kwargs["y_limit"] = [min([chart.y_limit[0] for chart in charts]),
            max([chart.y_limit[1] for chart in charts])]
        AxisChart.__init__(self, **kwargs)
        self.charts = charts[:]
        for chart in self.charts:
            chart.x_limit = self.x_limit
            chart.y_limit = self.y_limit
        self.labels = [chart.series_name for chart in self.charts]


    _paint_series = tkdisplay._multi_paint_series
    _draw_legend_symbols = tkdisplay._multi_draw_legend_symbols



def generate_random_color():
    return "#%02X%02X%02X" % (
     random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def get_limit(n):
    x = 10 ** math.floor(math.log(n, 10))
    return math.ceil(n / x) * x
