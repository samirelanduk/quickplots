from .display import Chart
from .data import *
import random
from tkinter import *

COLORS = ["#F15854", "#60BD68", "#5DA5DA", "#FAA43A",
 "#F17CB0", "#B2912F", "#B276B2", "#DECF3F", "#4D4D4D"]


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


    def _prepare_canvas(self, canvas):
        Chart._prepare_canvas(self, canvas)

        canvas.radius = min([canvas.plot_width, canvas.plot_height])
        if canvas.radius > 0:
            canvas.x_start = canvas.plot_margin + ((canvas.plot_width - canvas.radius) / 2)
            canvas.x_end = (canvas.chart_width - canvas.plot_margin) - ((canvas.plot_width - canvas.radius) / 2)
            canvas.y_start = canvas.title_height + canvas.plot_margin_top + ((canvas.plot_height - canvas.radius) / 2)
            canvas.y_end = canvas.height - canvas.plot_margin - ((canvas.plot_height - canvas.radius) / 2)

        if self.debug:
            canvas.create_rectangle(canvas.x_start, canvas.y_start,
             canvas.x_end, canvas.y_end, dash=(1,2))


    def _paint_series(self, canvas):
        if canvas.radius > 0:
            data_sum = sum(self.data)
            starts = [360 - ((sum(self.data[:i])/data_sum)*360) + 90
             for i,_ in enumerate(self.data, start=1)]
            extents = [(d/data_sum)*360 for d in self.data]

            for index, _ in enumerate(self.data):
                canvas.create_arc(
                 canvas.x_start,
                 canvas.y_start,
                 canvas.x_end,
                 canvas.y_end,
                 start=starts[index],
                 extent=extents[index],
                 width=1,
                 fill=self.colors[index],
                 outline=self.colors[index]
                )


    def _create_legend(self, canvas):
        Chart._create_legend(self, canvas)
        if self.legend:
            for index, _ in enumerate(self.data):
                canvas.create_rectangle(
                 (canvas.width - canvas.legend_width) + canvas.legend_x_margin + canvas.legend_padding,
                 canvas.legend_top_margin + (canvas.legend_row_height*index) + (canvas.legend_row_height / 6),
                 (canvas.width - canvas.legend_width) + canvas.legend_x_margin + (canvas.legend_row_height / 1.5) + canvas.legend_padding,
                 canvas.legend_top_margin + (canvas.legend_row_height*index) + (canvas.legend_row_height / (6/5)),
                 fill=self.colors[index]
                )



class AxisChart(Chart):
    """A chart with axes"""

    can_grid = True

    def __init__(self, x_limit=[0,1], x_ticks=None, x_tick_labels=None, x_label="",
     y_limit=[0,1], y_ticks=None, y_tick_labels=None, y_label="", grid=True, **kwargs):
        Chart.__init__(self, **kwargs)

        print(x_limit)
        self.x_limit = check_series_for_dates(x_limit)
        print(self.x_limit)
        self.x_ticks = x_limit if x_ticks is None else check_series_for_dates(x_ticks)
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


    def _prepare_canvas(self, canvas):
        Chart._prepare_canvas(self, canvas)

        canvas.tick_length = canvas.plot_margin / 4
        canvas.tick_label_length = canvas.plot_margin / 4
        canvas.axis_label_length = canvas.plot_margin / 2


    def _draw_grids(self, canvas):
        if self.grid:
            for tick in self.x_ticks:
                canvas.create_line(
                 _get_x_position(self, canvas, tick), canvas.height - canvas.plot_margin,
                 _get_x_position(self, canvas, tick), canvas.title_height + canvas.plot_margin_top,
                 dash=(2,2)
                )

            for tick in self.y_ticks:
                canvas.create_line(
                 canvas.plot_margin, _get_y_position(self, canvas, tick),
                 canvas.chart_width - canvas.plot_margin, _get_y_position(self, canvas, tick),
                 dash=(2,2)
                )


    def _draw_plot_bounds(self, canvas):
        #Splash some white paint around
        canvas.create_rectangle(
         0, 0,
         canvas.width, canvas.title_height + canvas.plot_margin_top,
         fill="#FFFFFF",
         width=0
        )
        canvas.create_rectangle(
         0, canvas.height - canvas.plot_margin,
         canvas.width, canvas.height,
         fill="#FFFFFF",
         width=0
        )
        canvas.create_rectangle(
         0, 0,
         canvas.plot_margin, canvas.height,
         fill="#FFFFFF",
         width=0
        )
        canvas.create_rectangle(
         canvas.width - (canvas.legend_width + canvas.plot_margin), 0,
         canvas.width, canvas.height,
         fill="#FFFFFF",
         width=0
        )

        if canvas.plot_width > 0 and canvas.plot_height > 0:
            #Plot bounds
            canvas.create_rectangle(
             canvas.plot_margin,
             canvas.title_height + canvas.plot_margin_top,
             canvas.chart_width - canvas.plot_margin,
             canvas.height - canvas.plot_margin
            )

            #Ticks
            for index, tick in enumerate(self.x_ticks):
                canvas.create_line(
                 _get_x_position(self, canvas, tick), canvas.height - canvas.plot_margin,
                 _get_x_position(self, canvas, tick), (canvas.height - canvas.plot_margin) + (canvas.tick_length * 0.8)
                )
                canvas.create_text(
                 _get_x_position(self, canvas, tick),
                 canvas.height - (canvas.axis_label_length + (canvas.tick_label_length / 2)),
                 text=self.x_tick_labels[index],
                 font="Bold %i" % (canvas.tick_label_length // 1.5)
                )

            for index, tick in enumerate(self.y_ticks):
                canvas.create_line(
                 canvas.plot_margin, _get_y_position(self, canvas, tick),
                 canvas.plot_margin - (0.8 * canvas.tick_length), _get_y_position(self, canvas, tick)
                )
                canvas.create_text(
                 canvas.axis_label_length + (canvas.tick_label_length / 2),
                 _get_y_position(self, canvas, tick),
                 text=self.y_tick_labels[index],
                 font="Bold %i" % (canvas.tick_label_length / 1.5)
                )

            #Axis labels
            canvas.create_text(
             canvas.plot_margin + (canvas.plot_width / 2),
             canvas.height - (canvas.axis_label_length / 2),
             text=self.x_label,
             font="Bold %i" % (canvas.axis_label_length / 1.7)
            )



class SingleSeriesAxisChart(AxisChart):
    """An axis chart with just one series on it"""

    def __init__(self, series, series_name="", **kwargs):
        if "x_limit" not in kwargs or kwargs["x_limit"] is None:
            kwargs["x_limit"] = min(list(zip(*series))[0]), max(list(zip(*series))[0])
        if "y_limit" not in kwargs or kwargs["y_limit"] is None:
            kwargs["y_limit"] = min(list(zip(*series))[1]), max(list(zip(*series))[1])
        AxisChart.__init__(self, **kwargs)

        self.series = type(series)([check_series_for_dates(t) for t in series])
        self.series_name = series_name
        self.labels = [self.series_name]


    def generate_moving_average(self, n):
        xs, ys = list(zip(*self.series))
        new_y = [sum(ys[i-(n-1):i+1]) / n for i,_ in enumerate(ys[n-1:], start=n-1)]
        new_x = xs[n-1:]
        series = list(zip(new_x, new_y))
        return LineChart(series, series_name=self.series_name + " moving average",
         color="#000000", x_limit=self.x_limit, x_ticks=self.x_ticks, x_tick_labels=self.x_tick_labels,
          x_label=self.x_label, y_limit=self.y_limit, y_ticks=self.y_ticks,
           y_tick_labels=self.y_tick_labels, y_label=self.y_label)



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


    def _paint_series(self, canvas):
        widths_in_pixels = (self.bar_width/(self.x_limit[1] - self.x_limit[0]) * canvas.plot_width)
        centers = [_get_x_position(self, canvas, val) for val, _ in self.series]
        offset = 0
        if self.align == "left":
            offset = widths_in_pixels / 2
        elif self.align == "right":
            offset = 0 - (widths_in_pixels / 2)
        centers = [val + offset for val in centers]
        heights = [_get_y_position(self, canvas, val) for _, val in self.series]

        for index, datum in enumerate(self.series):
            canvas.create_rectangle(
             centers[index] - (widths_in_pixels / 2),
             heights[index],
             centers[index] + (widths_in_pixels / 2),
             canvas.height - (canvas.plot_margin - 1),
             fill=self.color,
             width=self.edge_width
            )


    def _create_legend(self, canvas):
        SingleSeriesAxisChart._create_legend(self, canvas)
        if self.legend:
            canvas.create_rectangle(
             (canvas.width - canvas.legend_width) + canvas.legend_x_margin + canvas.legend_padding,
             canvas.legend_top_margin + (canvas.legend_row_height / 6),
             (canvas.width - canvas.legend_width) + canvas.legend_x_margin + (canvas.legend_row_height / 1.5) + canvas.legend_padding,
             canvas.legend_top_margin + (canvas.legend_row_height / (6/5)),
             fill=self.color
            )
            canvas.legend_top_margin += canvas.legend_row_height



class LineChart(SingleSeriesAxisChart):
    """A line chart"""

    def __init__(self, *args, color=None, width=2, style="-", **kwargs):
        SingleSeriesAxisChart.__init__(self, *args, **kwargs)

        if color is None:
            self.color = random.choice(COLORS)
        else:
            self.color = color

        self.width = width
        self.style = style


    def _paint_series(self, canvas):
        coordinates = []
        for datum in self.series:
            coordinates.append(_get_x_position(self, canvas, datum[0]))
            coordinates.append(_get_y_position(self, canvas, datum[1]))

        kwargs = {
         "width": self.width,
         "fill": self.color
        }

        if self.style == "--":
            kwargs["dash"] = (6,6)

        canvas.create_line(*coordinates, **kwargs)


    def _create_legend(self, canvas):
        SingleSeriesAxisChart._create_legend(self, canvas)
        if self.legend:
            args = [
             (canvas.width - canvas.legend_width) + canvas.legend_x_margin + canvas.legend_padding,
             canvas.legend_top_margin + (canvas.legend_row_height / 2),
             (canvas.width - canvas.legend_width) + canvas.legend_x_margin + (canvas.legend_row_height / 1.5) + canvas.legend_padding,
             canvas.legend_top_margin + (canvas.legend_row_height / 2)
            ]

            kwargs = {
             "width": self.width,
             "fill": self.color

            }

            if self.style == "--":
                kwargs["dash"] = (6,6)

            canvas.create_line(*args, **kwargs)
            canvas.legend_top_margin += canvas.legend_row_height



class ScatterChart(SingleSeriesAxisChart):

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


    def _paint_series(self, canvas):
        for datum in self.series:
            location = (_get_x_position(self, canvas, datum[0]), _get_y_position(self, canvas, datum[1]))

            if self.marker == "o":
                canvas.create_oval(
                 location[0] - (self.size / 2), location[1] - (self.size / 2),
                 location[0] + (self.size / 2), location[1] + (self.size / 2),
                 fill=self.color,
                 width=self.edge_width,
                 outline=self.edge_color
                )
            elif self.marker == "x":
                canvas.create_line(
                 location[0] - (self.size / 2), location[1] - (self.size / 2),
                 location[0] + (self.size / 2), location[1] + (self.size / 2),
                 fill=self.edge_color,
                 width=self.edge_width
                )
                canvas.create_line(
                 location[0] - (self.size / 2), location[1] + (self.size / 2),
                 location[0] + (self.size / 2), location[1] - (self.size / 2),
                 fill=self.edge_color,
                 width=self.edge_width
                )


    def _create_legend(self, canvas):
        SingleSeriesAxisChart._create_legend(self, canvas)
        if self.legend:
            if self.marker == "o":
                canvas.create_oval(
                 (canvas.width - canvas.legend_width) + canvas.legend_x_margin + canvas.legend_padding,
                 canvas.legend_top_margin + (canvas.legend_row_height / 6),
                 (canvas.width - canvas.legend_width) + canvas.legend_x_margin + (canvas.legend_row_height / 1.5) + canvas.legend_padding,
                 canvas.legend_top_margin + (canvas.legend_row_height / (6/5)),
                 fill=self.color,
                 outline=self.edge_color,
                 width=self.edge_width
                )
            elif self.marker == "x":
                canvas.create_line(
                 (canvas.width - canvas.legend_width) + canvas.legend_x_margin + canvas.legend_padding,
                 canvas.legend_top_margin + (canvas.legend_row_height / 6),
                 (canvas.width - canvas.legend_width) + canvas.legend_x_margin + (canvas.legend_row_height / 1.5) + canvas.legend_padding,
                 canvas.legend_top_margin + (canvas.legend_row_height / (6/5)),
                 fill=self.edge_color,
                 width=self.edge_width
                )
                canvas.create_line(
                 (canvas.width - canvas.legend_width) + canvas.legend_x_margin + canvas.legend_padding,
                 canvas.legend_top_margin + (canvas.legend_row_height / (6/5)),
                 (canvas.width - canvas.legend_width) + canvas.legend_x_margin + (canvas.legend_row_height / 1.5) + canvas.legend_padding,
                 canvas.legend_top_margin + (canvas.legend_row_height / 6),
                 fill=self.edge_color,
                 width=self.edge_width
                )
            canvas.legend_top_margin += canvas.legend_row_height



class MultiSeriesAxisChart(AxisChart):
    """An axis chart with more than one series on it."""

    def __init__(self, charts, **kwargs):
        if "x_limit" not in kwargs or kwargs["x_limit"] is None:
            kwargs["x_limit"] = [min([chart.x_limit[0] for chart in charts]),
            max([chart.x_limit[1] for chart in charts])]
        if "y_limit" not in kwargs or kwargs["y_limit"] is None:
            kwargs["y_limit"] = [min([chart.y_limit[0] for chart in charts]),
            max([chart.y_limit[1] for chart in charts])]
        print(kwargs)
        AxisChart.__init__(self, **kwargs)
        self.charts = charts
        self.labels = [chart.series_name for chart in self.charts]


    def _paint_series(self, canvas):
        for chart in self.charts:
            chart._paint_series(canvas)


    def _create_legend(self, canvas):
        for chart in self.charts:
            chart._create_legend(canvas)


def generate_random_color():
    return "#%02X%02X%02X" % (
     random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def _get_x_position(chart, canvas, value):
    x_distance = chart.x_limit[1] - chart.x_limit[0]
    val_distance = value - chart.x_limit[0]
    return canvas.plot_margin + ((val_distance / x_distance) * canvas.plot_width)


def _get_y_position(chart, canvas, value):
    y_distance = chart.y_limit[1] - chart.y_limit[0]
    val_distance = value - chart.y_limit[0]
    return canvas.height - (canvas.plot_margin + ((val_distance / y_distance) * canvas.plot_height))
