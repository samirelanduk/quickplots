import random
import matplotlib.pyplot as plt

COLORS = ["FF0000", "00FF00", "0000FF"]


def generate_random_color():
    return "%02X%02X%02X" % (
     random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))



class ChartCanvas:
    """A generic chart - a blank slate, capable of holding anything."""

    def __init__(self, title="", window_title=""):
        self.title = title
        self.window_title = window_title



    def show(self):
        self._generate().show()


    def save(self, path):
        self._generate().show()


    def render_svg(self):
        pass


    def _generate(self):
        """Get a Matplotlib representation of this object"""
        fig = plt.figure()
        fig.canvas.set_window_title(self.window_title)
        fig.title = self.title
        return fig





class Figure(ChartCanvas):
    """A container for multiple charts."""

    def __init__(self, charts, row_num, col_num, title="", window_title=""):
        ChartCanvas.__init__(self, title=title, window_title=window_title)
        #Are the dimensions sensible?
        assert row_num * col_num >= len(charts), \
         "There are too many charts for the dimensions given."

        self.charts = charts




class Chart(ChartCanvas):
    """A generic chart, containing a single visualisation."""

    _can_legend = False

    def __init__(self, legend=False, title="", window_title=""):
        ChartCanvas.__init__(self, title=title, window_title=window_title)
        self.legend = legend




class PieChart(Chart):
    """A pie chart. You know what a pie chart is."""

    _can_legend = True

    def __init__(self, data, labels=None, colors=None, line_width=1,
     legend=False, title="", window_title=""):

        Chart.__init__(self, legend=legend, title=title, window_title=window_title)

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

    def __init__(self, x_range=[0,1], x_ticks=[], x_tick_labels=None, x_title="",
     y_range=[0,1], y_ticks=[], y_tick_labels=None, y_title="", grid=True,
      legend=False, title="", window_title=""):

        Chart.__init__(self, title=title, window_title=window_title)

        self.x_range = x_range
        self.x_ticks = x_ticks
        if x_tick_labels is None:
            self.x_tick_labels = [str(tick) for tick in self.x_ticks]
        else:
            self.x_tick_labels = x_tick_labels
        self.x_title = x_title

        self.y_range = y_range
        self.y_ticks = y_ticks
        if y_tick_labels is None:
            self.y_tick_labels = [str(tick) for tick in self.y_ticks]
        else:
            self.y_tick_labels = y_tick_labels
        self.y_title = y_title

        self.grid = grid




class SingleSeriesAxisChart(AxisChart):
    """An axis chart with a single series on it.

    The default axis ranges for an axis chart with a series are the series limits."""

    _can_legend = True

    def __init__(self, series, series_name = "",
     x_range=None, x_ticks=[], x_tick_labels=None, x_title="",
      y_range=None, y_ticks=[], y_tick_labels=None, y_title="", grid=True,
       legend=False, title="", window_title=""):

       #Don't want to use AxisChart's method for generating x_range, as we can
       #do better now that we know the series. So, assign these BEFORE calling
       #the super constructor.
        if x_range is None:
            self.x_range = [min(list(zip(*series))[0]), max(list(zip(*series))[0])]
        else:
            self.x_range = x_range

        if y_range is None:
            self.y_range = [min(list(zip(*series))[1]), max(list(zip(*series))[1])]
        else:
            self.y_range = y_range

        AxisChart.__init__(self, x_range=self.x_range, y_range=self.y_range,
         x_ticks=x_ticks, x_tick_labels=x_tick_labels, x_title=x_title,
          y_ticks=y_ticks, y_tick_labels=y_tick_labels, y_title=y_title, grid=True,
           legend=legend, title=title, window_title=window_title)

        self.series = series
        self.series_name = series_name




class MultiSeriesAxisChart(AxisChart):
    """An axis chart with multiple series on it.

    The default axis ranges for an axis chart with multiple series will be the
    most extreme limits of its series."""

    _can_legend = True


    def __init__(self, charts,
     x_range=None, x_ticks=[], x_tick_labels=None, x_title="",
      y_range=None, y_ticks=[], y_tick_labels=None, y_title="", grid=True,
       legend=False, title="", window_title=""):

        #Again - don't want to use AxisChart's method for generating x_range,
        #as we can do better now that we know the series. So, assign these BEFORE
        #calling the super constructor.
         if x_range is None:
             self.x_range = [min([chart.x_range[0] for chart in charts]),
              max([chart.x_range[1] for chart in charts])]
         else:
             self.x_range = x_range

         if y_range is None:
             self.y_range = [min([chart.y_range[0] for chart in charts]),
              max([chart.y_range[1] for chart in charts])]
         else:
             self.y_range = y_range

         AxisChart.__init__(self, x_range=self.x_range, y_range=self.y_range,
          x_ticks=x_ticks, x_tick_labels=x_tick_labels, x_title=x_title,
           y_ticks=y_ticks, y_tick_labels=y_tick_labels, y_title=y_title, grid=True,
            legend=legend, title=title, window_title=window_title)




class LineChart(SingleSeriesAxisChart):
    """A line chart."""

    _can_legend = True

    def __init__(self, series, color=None, width=1, style="-",
     series_name="",
      x_range=None, x_ticks=[], x_tick_labels=None, x_title="",
       y_range=None, y_ticks=[], y_tick_labels=None, y_title="", grid=True,
        legend=False, title="", window_title=""):

        SingleSeriesAxisChart.__init__(self, series=series, series_name=series_name,
         x_range=x_range, x_ticks=x_ticks, x_tick_labels=x_tick_labels, x_title=x_title,
          y_range=y_range, y_ticks=y_ticks, y_tick_labels=y_tick_labels, y_title=y_title, grid=True,
            legend=legend, title=title, window_title=window_title)

        if color is None:
            self.color = random.choice(COLORS)
        else:
            self.color = color

        self.width = width
        self.style = style




class BarChart(SingleSeriesAxisChart):
    """A bar chart."""

    _can_legend = True

    def __init__(self, series,
     color=None, bar_width=1, align="center", edge_width=1, edge_color="#000000",
      series_name="",
       x_range=None, x_ticks=[], x_tick_labels=None, x_title="",
        y_range=None, y_ticks=[], y_tick_labels=None, y_title="", grid=True,
         legend=False, title="", window_title=""):

        SingleSeriesAxisChart.__init__(self, series=series, series_name=series_name,
         x_range=x_range, x_ticks=x_ticks, x_tick_labels=x_tick_labels, x_title=x_title,
          y_range=y_range, y_ticks=y_ticks, y_tick_labels=y_tick_labels, y_title=y_title, grid=True,
            legend=legend, title=title, window_title=window_title)

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

    _can_legend = True

    def __init__(self, series,
     color=None, marker="x", size=30, edge_width=1, edge_color="#000000",
      series_name="",
       x_range=None, x_ticks=[], x_tick_labels=None, x_title="",
        y_range=None, y_ticks=[], y_tick_labels=None, y_title="", grid=True,
         legend=False, title="", window_title=""):

        SingleSeriesAxisChart.__init__(self, series=series, series_name=series_name,
         x_range=x_range, x_ticks=x_ticks, x_tick_labels=x_tick_labels, x_title=x_title,
          y_range=y_range, y_ticks=y_ticks, y_tick_labels=y_tick_labels, y_title=y_title, grid=True,
            legend=legend, title=title, window_title=window_title)

        if color is None:
            self.color = random.choice(COLORS)
        else:
            self.color = color

        self.marker = marker
        self.size = size
        self.edge_width = edge_width
        self.edge_color = edge_color
