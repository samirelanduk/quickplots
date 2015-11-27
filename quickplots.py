import random
from tkinter import *

COLORS = ["#F15854", "#60BD68", "#5DA5DA", "#FAA43A", "#F17CB0", "#B2912F", "#B276B2", "#DECF3F", "#4D4D4D"]

DEFAULT_DIMENSIONS = [900, 700]


def generate_random_color():
    return "#%02X%02X%02X" % (
     random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


class PlotCanvas(Canvas):

    def __init__(self, master, chart, **kwargs):

        Canvas.__init__(self, master, **kwargs)
        self.bind("<Configure>", self.on_resize)
        if isinstance(chart, AxisChart):
            self.bind("<B1-Motion>", self.on_b1)
            self.bind("<Button-1>", self.on_b1)
            self.bind("<ButtonRelease-1>", self.on_bup)
        self.chart = chart


    def on_resize(self, event):
        self.chart._paint_canvas(self)


    def on_b1(self, event):
        self.chart._paint_canvas(self)
        if event.x > self.plot_margin and event.x < self.plot_margin + self.plot_width and\
         event.y > self.title_height + self.plot_top_margin and\
          event.y < self.title_height + self.plot_top_margin + self.plot_height:

            self.create_line(
             event.x,
             self.height - self.plot_margin,
             event.x,
             self.title_height + self.plot_top_margin,
             dash=(1,1),
             fill="red"
            )
            self.create_line(
             self.plot_margin,
             event.y,
             self.plot_margin + self.plot_width,
             event.y,
             dash=(1,1),
             fill="red"
            )
            self.create_text(
             5,
             self.height - 20,
             font=("Arial 7"),
             text="x: %f" %
              ((((event.x - self.plot_margin) / self.plot_width) *
               (self.chart.x_limit[1] - self.chart.x_limit[0])) + self.chart.x_limit[0]),
             justify=LEFT,
             anchor=W
            )
            self.create_text(
             5,
             self.height - 10,
             font=("Arial 7"),
             text="y: %f" %
              ((self.chart.y_limit[1] - self.chart.y_limit[0]) -
               (((event.y - (self.plot_top_margin + self.title_height)) / self.plot_height)
                * (self.chart.y_limit[1] - self.chart.y_limit[0])) + self.chart.y_limit[0]),
             justify=LEFT,
             anchor=W
            )

    def on_bup(self, event):
        self.chart._paint_canvas(self)



class GenericChart:
    """A generic chart - a blank slate, capable of holding anything."""

    def __init__(self, title="", window_title="", dimensions=DEFAULT_DIMENSIONS):
        self.title = title
        self.window_title = window_title
        self.dimensions = dimensions


    def _get_window(self):
        root = Tk()
        root.title(self.window_title)
        root.geometry("%ix%i" % (self.dimensions[0], self.dimensions[1]))

        root.frame = Frame(root)
        root.frame.pack(fill=BOTH, expand=YES)
        title_label = Label(root.frame, text=self.title, font=("Helvetica", 20))
        title_label.pack()

        return root


    def show(self):
        self._get_window().mainloop()




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

    def _get_window(self):
        root = GenericChart._get_window(self)

        #Add frame to hold the canvases
        grid = Frame(root.frame)
        grid.pack(fill=BOTH, expand=YES, padx=(15, 15), pady=(15, 15))
        for row in range(self.row_num):
            Grid.rowconfigure(grid, row, weight=1)
        for col in range(self.col_num):
            Grid.columnconfigure(grid, col, weight=1)

        #Add the charts
        for row in range(self.row_num):
            for col in range(self.col_num):
                print("%i, %i" % (row, col))
                if (row * self.col_num) + col < len(self.charts):
                    this_chart = self.charts[(row * self.col_num) + col]
                    canvas = PlotCanvas(grid, this_chart, background="#FFFFFF")
                    canvas.grid(row=row, column=col, sticky=N+S+E+W)
                    this_chart._paint_canvas(canvas)


        return root




class Chart(GenericChart):
    """A generic chart, containing a single visualisation."""

    def __init__(self, chart_title="", legend=False, margin=30,
     title="", window_title="", dimensions=DEFAULT_DIMENSIONS):
        GenericChart.__init__(self, title=title, window_title=window_title, dimensions=dimensions)

        self.chart_title = chart_title
        self.legend = legend
        self.margin = margin


    def _paint_canvas(self, canvas):
        canvas.delete("all")

        #Get canvas parameters
        canvas.width = canvas.winfo_width()
        canvas.height = canvas.winfo_height()


        #Get chart parameters
        canvas.legend_width = 250 if self.legend else 0
        canvas.chart_width = canvas.width - canvas.legend_width

        title = canvas.create_text(
         (canvas.width - canvas.legend_width)/2,
         int(canvas.width/25),
         font="Tahoma %i bold" %
          (int(canvas.chart_width/30) - int(len(self.chart_title)/10)),
         text=self.chart_title
        )
        canvas.title_height = canvas.bbox(title)[3]
        canvas.chart_height = canvas.height - canvas.title_height

        #canvas.create_line(canvas.chart_width, 0, canvas.chart_width, canvas.height, dash=(3,3))
        #canvas.create_line(0, canvas.title_height, canvas.chart_width, canvas.title_height, dash=(3,3))


        #Get plot parameters
        canvas.plot_margin = 75
        canvas.plot_top_margin = 10
        canvas.plot_width = canvas.chart_width - (2 * canvas.plot_margin)
        canvas.plot_height = canvas.chart_height - (canvas.plot_margin + canvas.plot_top_margin)

        #canvas.create_rectangle(canvas.plot_margin, canvas.height-canvas.plot_margin, canvas.chart_width-canvas.plot_margin, canvas.title_height+canvas.plot_top_margin, dash=(2,2))


    def _get_window(self):
        root = GenericChart._get_window(self)
        root.frame.canvas = PlotCanvas(root.frame, self, background="#FFFFFF")
        root.frame.canvas.pack(fill=BOTH, expand=YES, padx=(self.margin,self.margin), pady=(self.margin/2,self.margin))
        self._paint_canvas(root.frame.canvas)

        return root




class PieChart(Chart):
    """A pie chart. You know what a pie chart is."""

    def __init__(self, data, labels=None, colors=None, line_width=0,
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

    def _paint_canvas(self, canvas):
        Chart._paint_canvas(self, canvas)
        radius = min([canvas.plot_width, canvas.plot_height])
        if radius > 0:

            #Calculate pie bounds
            x_start = canvas.plot_margin + ((canvas.plot_width - radius) / 2)
            x_end = (canvas.chart_width - canvas.plot_margin) - ((canvas.plot_width - radius) / 2)
            y_start = canvas.title_height + canvas.plot_top_margin + ((canvas.plot_height - radius) / 2)
            y_end = canvas.height - canvas.plot_margin - ((canvas.plot_height - radius) / 2)
            #canvas.create_rectangle(x_start, y_start, x_end, y_end, dash=(1,2))
            #Get start points and extents
            data_sum = sum(self.data)
            starts = [360 - ((sum(self.data[:i])/data_sum)*360) + 90 for i,_ in enumerate(self.data, start=1)]
            extents = [(d/data_sum)*360 for d in self.data]

            for index, _ in enumerate(self.data):
                canvas.create_arc(
                 x_start,
                 y_start,
                 x_end,
                 y_end,
                 start=starts[index],
                 extent=extents[index],
                 width=self.line_width,
                 fill=self.colors[index],
                 outline="black" if self.line_width > 0 else self.colors[index]
                )

                if self.legend:
                    canvas.create_rectangle(
                     (canvas.width - canvas.legend_width) + 10,
                     80 + (30*index) + 5,
                     (canvas.width - canvas.legend_width) + 30,
                     80 + (30*index) + 25,
                     fill=self.colors[index]
                    )

                    canvas.create_text(
                     (canvas.width - canvas.legend_width) + 35,
                     80 + (30*index) + 15,
                     font="Tahoma %i" % 10,
                     text=self.labels[index],
                     justify=LEFT,
                     anchor=W
                    )
            if self.legend:
                canvas.create_rectangle(
                 (canvas.width - canvas.legend_width) + 2,
                 80,
                 canvas.width - 10,
                 80 + (30 * (len(self.data) - 1)) + 35
                )


    def _get_window(self):
        root = Chart._get_window(self)
        self._paint_canvas(root.frame.canvas)

        return root



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

    def _get_x_axis_location(self, value, canvas):
        x_distance = self.x_limit[1] - self.x_limit[0]
        val_distance = value - self.x_limit[0]
        return canvas.plot_margin + ((val_distance / x_distance) * canvas.plot_width)


    def _get_y_axis_location(self, value, canvas):
        y_distance = self.y_limit[1] - self.y_limit[0]
        val_distance = value - self.y_limit[0]
        return canvas.height - (canvas.plot_margin + ((val_distance / y_distance) * canvas.plot_height))

    def _paint_canvas(self, canvas):
        Chart._paint_canvas(self, canvas)


        if canvas.plot_width > 0 and canvas.plot_height > 0:
            canvas.create_rectangle(
             canvas.plot_margin,
             canvas.title_height + canvas.plot_top_margin,
             canvas.chart_width - canvas.plot_margin,
             canvas.height - canvas.plot_margin
            )

            for index, xtick in enumerate(self.x_ticks):
                if xtick >= self.x_limit[0] and xtick <= self.x_limit[1]:
                    canvas.create_line(
                     self._get_x_axis_location(xtick, canvas),
                     canvas.height - canvas.plot_margin,
                     self._get_x_axis_location(xtick, canvas),
                     canvas.height - (canvas.plot_margin - 10)
                    )

                    canvas.create_text(
                     self._get_x_axis_location(xtick, canvas),
                     canvas.height - (canvas.plot_margin - 20),
                     font="Tahoma %i" % 8,
                     text=self.x_tick_labels[index],
                    )

                    if self.grid and xtick != self.x_limit[0] and xtick != self.x_limit[1]:
                        canvas.create_line(
                         self._get_x_axis_location(xtick, canvas),
                         canvas.height - canvas.plot_margin,
                         self._get_x_axis_location(xtick, canvas),
                         canvas.title_height + canvas.plot_top_margin,
                         dash=(3,3)
                        )
            if self.x_label:
                canvas.create_text(
                 canvas.plot_margin + (canvas.plot_width / 2),
                 (canvas.height - canvas.plot_margin) + 40,
                 font="Bold",
                 text=self.x_label
                )

            for index, ytick in enumerate(self.y_ticks):
                if ytick >= self.y_limit[0] and ytick <= self.y_limit[1]:
                    canvas.create_line(
                     canvas.plot_margin,
                     self._get_y_axis_location(ytick, canvas),
                     canvas.plot_margin - 10,
                     self._get_y_axis_location(ytick, canvas)
                    )

                    canvas.create_text(
                     canvas.plot_margin - 15,
                     self._get_y_axis_location(ytick, canvas),
                     font="Tahoma %i" % 8,
                     text=self.y_tick_labels[index],
                     justify=RIGHT,
                     anchor=E
                    )

                    if self.grid and ytick != self.y_limit[0] and ytick != self.y_limit[1]:
                        canvas.create_line(
                         canvas.plot_margin,
                         self._get_y_axis_location(ytick, canvas),
                         canvas.plot_margin + canvas.plot_width,
                         self._get_y_axis_location(ytick, canvas),
                         dash=(3,3)
                        )


    def _generate_window(self):
        root = Chart._generate_window(self)
        self._paint_canvas(root.frame.canvas)
        return root




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
            self.x_limit = min(list(zip(*series))[0]), max(list(zip(*series))[0])
        else:
            self.x_limit = x_limit

        if y_limit is None:
            self.y_limit = min(list(zip(*series))[1]), max(list(zip(*series))[1])
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
