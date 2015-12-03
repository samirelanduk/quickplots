from .display import Chart
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


    def _debug_lines(self, canvas):
        Chart._debug_lines(self, canvas)
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
        if self.legend:
            for index, _ in enumerate(self.data):
                canvas.create_rectangle(
                 (canvas.width - canvas.legend_width) + canvas.legend_x_margin + canvas.legend_padding,
                 canvas.legend_top_margin + (canvas.legend_row_height*index) + (canvas.legend_row_height / 6),
                 (canvas.width - canvas.legend_width) + canvas.legend_x_margin + (canvas.legend_row_height / 1.5) + canvas.legend_padding,
                 canvas.legend_top_margin + (canvas.legend_row_height*index) + (canvas.legend_row_height / (6/5)),
                 fill=self.colors[index]
                )

                canvas.create_text(
                 (canvas.width - canvas.legend_width) + canvas.legend_x_margin + (2 * canvas.legend_padding) + (canvas.legend_row_height / 1.5),
                 canvas.legend_top_margin + (canvas.legend_row_height*index) + (canvas.legend_row_height / 2),
                 font="Tahoma %i" % 10,
                 text=self.labels[index],
                 justify=LEFT,
                 anchor=W
                )
def generate_random_color():
    return "#%02X%02X%02X" % (
     random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
