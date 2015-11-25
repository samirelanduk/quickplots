import random
import matplotlib.pyplot as plt

COLORS = ["FF0000", "00FF00", "0000FF"]

DEFAULT_DIMENSIONS = [300, 200]]


def generate_random_color():
    return "%02X%02X%02X" % (
     random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))



class GenericChart:
    """A generic chart - a blank slate, capable of holding anything."""

    def __init__(self, title="", window_title="", dimensions=DEFAULT_DIMENSIONS):
        self.title = title
        self.window_title = window_title
        self.dimensions = dimensions




class Figure(GenericChart):
    """A container for multiple charts."""

    def __init__(self, charts, row_num, col_num,
     title="", window_title="", dimensions=DEFAULT_DIMENSIONS):
        GenericChart.__init__(self, title=title, window_title=window_title, dimensions=dimensions)

        #Are the numbers of rows and columns sensible?
        assert row_num * col_num >= len(charts), \
         "There are too many charts for the rows and columns given."

        self.charts = charts
        self.row_num = row_num
        self.col_num = col_num




class Chart(GenericChart):
    """A generic chart, containing a single visualisation."""

    def __init__(self, chart_title="", legend=False, margin=30,
     title="", window_title="", dimensions=DEFAULT_DIMENSIONS):
        GenericChart.__init__(self, title=title, window_title=window_title, dimensions=dimensions)

        self.chart_title = chart_title
        self.legend = legend
        self.margin = margin




class PieChart(Chart):
    """A pie chart. You know what a pie chart is."""

    def __init__(self, data, labels=None, colors=None, line_width=1,
     chart_title="", legend=False, margin=30,
      title="", window_title="", dimensions=DEFAULT_DIMENSIONS):

        Chart.__init__(self, chart_title=chart_title, legend=legend, margin=margin,
         title=title, window_title=window_title, dimensions=dimensions)

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

        self.line_width = line_width




class AxisChart(Chart):
    """A chart with an axis (pretty much anything except pie charts).

    The default axis ranges for a generic axis chart with no data are 0 and 1."""

    def __init__(self, x_limit=[0,1], x_ticks=[], x_tick_labels=None, x_label="",
     y_limit=[0,1], y_ticks=[], y_tick_labels=None, y_label="", grid=True,
      chart_title="", legend=False, margin=30,
       title="", window_title="", dimensions=DEFAULT_DIMENSIONS):

        Chart.__init__(self, chart_title=chart_title, legend=legend, margin=margin,
         title=title, window_title=window_title, dimensions=dimensions)

        self.x_limit = x_limit
        self.x_ticks = x_ticks
        if x_tick_labels is None:
            self.x_tick_labels = [str(tick) for tick in self.x_ticks]
        else:
            assert len(x_tick_labels) == len(x_ticks), "Not one label per x-tick."
            self.x_tick_labels = x_tick_labels
        self.x_label = x_label

        self.y_limit = y_limit
        self.y_ticks = y_ticks
        if y_tick_labels is None:
            self.y_tick_labels = [str(tick) for tick in self.y_ticks]
        else:
            assert len(y_tick_labels) == len(y_ticks), "Not one label per y-tick."
            self.y_tick_labels = y_tick_labels
        self.y_label = y_label

        self.grid = grid




class SingleSeriesAxisChart(AxisChart):
    """An axis chart with a single series on it.

    The default axis ranges for an axis chart with a series are the series limits."""

    def __init__(self, series, series_name = "",
     x_limit=None, x_ticks=[], x_tick_labels=None, x_label="",
      y_limit=None, y_ticks=[], y_tick_labels=None, y_label="", grid=True,
       chart_title="", legend=False, margin=30,
        title="", window_title="", dimensions=DEFAULT_DIMENSIONS):


       #Don't want to use AxisChart's method for generating xy_limit, as we can
       #do better now that we know the series. So, assign these BEFORE calling
       #the super constructor.
        if x_limit is None:
            self.x_limit = [min(list(zip(*series))[0]), max(list(zip(*series))[0])]
        else:
            self.x_limit = x_limit

        if y_limit is None:
            self.y_limit = [min(list(zip(*series))[1]), max(list(zip(*series))[1])]
        else:
            self.y_limit = y_limit

        AxisChart.__init__(self, x_limit=self.x_limit, y_limit=self.y_limit,
         x_ticks=x_ticks, x_tick_labels=x_tick_labels, x_label=x_label,
          y_ticks=y_ticks, y_tick_labels=y_tick_labels, y_label=y_label, grid=True,
           chart_title=chart_title, legend=legend, margin=margin,
            title=title, window_title=window_title, dimensions=dimensions)

        self.series = series
        self.series_name = series_name




class MultiSeriesAxisChart(AxisChart):
    """An axis chart with multiple series on it.

    The default axis ranges for an axis chart with multiple series will be the
    most extreme limits of its series."""

    def __init__(self, charts,
     x_limit=None, x_ticks=[], x_tick_labels=None, x_label="",
      y_limit=None, y_ticks=[], y_tick_labels=None, y_label="", grid=True,
       chart_title="", legend=False, margin=30,
        title="", window_title="", dimensions=DEFAULT_DIMENSIONS):

        #Again - don't want to use AxisChart's method for generating x_range,
        #as we can do better now that we know the series. So, assign these BEFORE
        #calling the super constructor.
        if x_limit is None:
            self.x_limit = [min([chart.x_limit[0] for chart in charts]),
            max([chart.x_limit[1] for chart in charts])]
        else:
            self.x_limit = x_limit

        if y_limit is None:
            self.y_limit = [min([chart.y_limit[0] for chart in charts]),
            max([chart.y_limit[1] for chart in charts])]
        else:
            self.y_limit = y_limit

        AxisChart.__init__(self, x_limit=self.x_limit, y_limit=self.y_limit,
         x_ticks=x_ticks, x_tick_labels=x_tick_labels, x_label=x_label,
          y_ticks=y_ticks, y_tick_labels=y_tick_labels, y_label=y_label, grid=True,
           chart_title=chart_title, legend=legend, margin=margin,
            title=title, window_title=window_title, dimensions=dimensions)

        self.charts = charts




class LineChart(SingleSeriesAxisChart):
    """A line chart."""

    def __init__(self, series, color=None, width=1, style="-",
     series_name="",
      x_limit=None, x_ticks=[], x_tick_labels=None, x_label="",
       y_limit=None, y_ticks=[], y_tick_labels=None, y_label="", grid=True,
        chart_title="", legend=False, margin=30,
         title="", window_title="", dimensions=DEFAULT_DIMENSIONS):

        SingleSeriesAxisChart.__init__(self, series=series, series_name=series_name,
         x_limit=x_limit, x_ticks=x_ticks, x_tick_labels=x_tick_labels, x_label=x_label,
          y_limit=y_limit, y_ticks=y_ticks, y_tick_labels=y_tick_labels, y_label=y_label, grid=True,
           chart_title=chart_title, legend=legend, margin=margin,
            title=title, window_title=window_title, dimensions=dimensions)

        if color is None:
            self.color = random.choice(COLORS)
        else:
            self.color = color

        self.width = width
        self.style = style




class BarChart(SingleSeriesAxisChart):
    """A bar chart."""

    def __init__(self, series,
     color=None, bar_width=1, align="center", edge_width=1, edge_color="#000000",
      series_name="",
       x_limit=None, x_ticks=[], x_tick_labels=None, x_label="",
        y_limit=None, y_ticks=[], y_tick_labels=None, y_label="", grid=True,
         chart_title="", legend=False, margin=30,
          title="", window_title="", dimensions=DEFAULT_DIMENSIONS):

        SingleSeriesAxisChart.__init__(self, series=series, series_name=series_name,
         x_limit=x_limit, x_ticks=x_ticks, x_tick_labels=x_tick_labels, x_label=x_label,
          y_limit=y_limit, y_ticks=y_ticks, y_tick_labels=y_tick_labels, y_label=y_label, grid=True,
           chart_title=chart_title, legend=legend, margin=margin,
            title=title, window_title=window_title, dimensions=dimensions)

        if color is None:
            self.color = random.choice(COLORS)
        else:
            self.color = color

        self.bar_width = bar_width
        self.align = align
        self.edge_width = edge_width
        self.edge_color = edge_color




class ScatterChart(SingleSeriesAxisChart):
    """A scatter chart."""

    def __init__(self, series,
     color=None, marker="x", size=30, edge_width=1, edge_color="#000000",
      series_name="",
       x_limit=None, x_ticks=[], x_tick_labels=None, x_label="",
        y_limit=None, y_ticks=[], y_tick_labels=None, y_label="", grid=True,
         chart_title="", legend=False, margin=30,
          title="", window_title="", dimensions=DEFAULT_DIMENSIONS):

        SingleSeriesAxisChart.__init__(self, series=series, series_name=series_name,
         x_limit=x_limit, x_ticks=x_ticks, x_tick_labels=x_tick_labels, x_label=x_label,
          y_limit=y_limit, y_ticks=y_ticks, y_tick_labels=y_tick_labels, y_label=y_label, grid=True,
           chart_title=chart_title, legend=legend, margin=margin,
            title=title, window_title=window_title, dimensions=dimensions)

        if color is None:
            self.color = random.choice(COLORS)
        else:
            self.color = color

        self.marker = marker
        self.size = size
        self.edge_width = edge_width
        self.edge_color = edge_color
