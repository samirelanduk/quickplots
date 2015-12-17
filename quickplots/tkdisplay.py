from tkinter import *
from .data import *
import math
import datetime

class ChartCanvas(Canvas):
    """A tkinter canvas that has an associated chart, and knows how to draw that chart"""

    def __init__(self, master, chart, **kwargs):
        Canvas.__init__(self, master, **kwargs)
        self.chart = chart
        self.bind("<Configure>", self.request_repaint)
        if chart.can_grid:
            self.bind("<B1-Motion>", self.on_click)
            self.bind("<Button-1>", self.on_click)
            self.bind("<ButtonRelease-1>", self.on_unclick)


    def lower_font(self, font):
        if font > 100:
            return font - 10
        elif font > 50:
            return font - 5
        elif font > 10:
            return font - 2
        elif font > 1:
            return font - 1
        else:
            return font - 0.1


    def get_font_size(self, text, width=None, height=None, font_style="Tahoma"):
        """Get the font size required to make text fit a bbox"""
        if width is None:
            width  = self.width
        if height is None:
            height = self.height
        font_size = 100
        t = self.scratch_canvas.create_text(0, 0, text=text, font="%s %i" % (font_style, font_size))

        while ((((self.scratch_canvas.bbox(t)[2] - (font_size / 9)) -
         (self.scratch_canvas.bbox(t)[0] + (font_size / 20))) > width) or
          (((self.scratch_canvas.bbox(t)[3] - (font_size / 5)) -
           (self.scratch_canvas.bbox(t)[1] + (font_size / 5))) > height)) and font_size > 0:
            font_size = self.lower_font(font_size)
            if font_size > 0:
                self.delete(t)
                t = self.scratch_canvas.create_text(0, 0, text=text, font="%s %i" % (font_style, font_size))
        if font_size <= 0:
            self.delete(t)
        return font_size


    def create_text(self, *args, width=None, height=None, font_style="Tahoma", **kwargs):
        if width is None and height is None:
            Canvas.create_text(self, *args, **kwargs)

        else:
            #There are boundary specifications for this text
            if width is None:
                width  = self.width
            if height is None:
                height = self.height

            Canvas.create_text(self, *args, font="%s %i" % (font_style, self.get_font_size(kwargs["text"], width, height, font_style)), **kwargs)


    def request_repaint(self, event):
        start = datetime.datetime.now()
        self.chart._prepare_canvas(self)
        one = datetime.datetime.now()
        self.chart._draw_grids(self)
        two = datetime.datetime.now()
        self.chart._paint_series(self)
        three = datetime.datetime.now()
        self.chart._draw_plot_bounds(self)
        four = datetime.datetime.now()
        self.chart._write_title(self)
        five = datetime.datetime.now()
        self.chart._create_legend(self)
        six = datetime.datetime.now()
        self.chart._debug_lines(self)
        end = datetime.datetime.now()

        if self.chart.debug:
            print("Prepare canvas: %i milliseconds." % (((one-start).seconds * 1000) + (one-start).microseconds / 1000))
            print("Draw grids: %i milliseconds." % (((two-one).seconds * 1000) + (two-one).microseconds / 1000))
            print("Paint series: %i milliseconds." % (((three-two).seconds * 1000) + (three-two).microseconds / 1000))
            print("Draw plot bounds: %i milliseconds." % (((four-three).seconds * 1000) + (four-three).microseconds / 1000))
            print("Write title: %i milliseconds." % (((five-four).seconds * 1000) + (five-four).microseconds / 1000))
            print("Create legend: %i milliseconds." % (((six-five).seconds * 1000) + (six-five).microseconds / 1000))
            print("Debug lines: %i milliseconds." % (((end-six).seconds * 1000) + (end-six).microseconds / 1000))
            print("TOTAL REPAINT TIME: %i milliseconds.\n" % (((end-start).seconds * 1000) + (end-start).microseconds / 1000))

    def on_click(self, event):
        self.request_repaint(self)
        if event.x > self.plot_margin_x and event.x < self.plot_margin_x + self.plot_width + 1 and\
         event.y > self.title_height + self.plot_margin_top and\
          event.y < self.title_height + self.plot_margin_top + self.plot_height + 2:

            self.create_line(
             event.x - 1,
             self.height - self.plot_margin_bottom,
             event.x - 1,
             self.title_height + self.plot_margin_top,
             dash=(1,1),
             fill="red"
            )
            self.create_line(
             self.plot_margin_x,
             event.y - 1,
             self.plot_margin_x + self.plot_width,
             event.y - 1,
             dash=(1,1),
             fill="red"
            )

            x_text = "x: %s" % _get_x_value(self.chart, self, event.x)
            self.label_canvas.create_text(
             self.label_canvas.x_start,
             self.label_canvas.line1_mid,
             text=x_text,
             anchor=W,
             font="Tahoma %i" % int(self.get_font_size(
              x_text,
              width=self.label_canvas.winfo_width() - self.label_canvas.x_start,
              height=self.label_canvas.line1_end - self.label_canvas.line1_start
             ))
            )

            y_text = "y: %s" % _get_y_value(self.chart, self, event.y)
            self.label_canvas.create_text(
             self.label_canvas.x_start,
             self.label_canvas.line2_mid,
             text=y_text,
             anchor=W,
             font="Tahoma %i" % int(self.get_font_size(
              y_text,
              width=self.label_canvas.winfo_width() - self.label_canvas.x_start,
              height=self.label_canvas.line2_end - self.label_canvas.line2_start
             ))
            )


    def on_unclick(self, event):
        self.request_repaint(self)
        self.label_canvas.delete("all")




#Generic methods
def show(chart):
    """Create a window and canvas for the chart 'self'"""
    root = Tk()
    root.title(chart.window_title)
    root.geometry("%ix%i" % (chart.window_dimensions[0], chart.window_dimensions[1]))

    root.frame = Frame(root, background=chart.background_color, bd=0)
    root.frame.pack(fill=BOTH, expand=YES)

    root.frame.top_margin = Canvas(root.frame, background=chart.background_color, height=chart.canvas_margin, bd=-1, highlightthickness=0)
    root.frame.top_margin.pack(fill=BOTH)

    root.frame.canvas = ChartCanvas(root.frame, chart, background="#FFFFFF")
    root.frame.canvas.label_canvas = root.frame.top_margin
    root.frame.canvas.scratch_canvas = Canvas()
    root.frame.canvas.pack(fill=BOTH, expand=YES, padx=chart.canvas_margin, pady=0)

    root.frame.bottom_margin = Frame(root.frame, background=chart.background_color, height=chart.canvas_margin)
    root.frame.bottom_margin.pack(fill=BOTH)

    root.mainloop()


def _empty(chart, canvas):
    pass


def _chart_prepare_canvas(chart, canvas):
    canvas.delete("all")
    canvas.label_canvas.delete("all")
    #Get the canvas dimensions
    canvas.width = canvas.winfo_width()
    canvas.height = canvas.winfo_height()

    #Get the chart area dimensions
    canvas.title_height = canvas.height / 10
    canvas.legend_width = canvas.width / 4 if chart.legend else 0
    canvas.chart_width = canvas.width - canvas.legend_width
    canvas.chart_height = canvas.height - canvas.title_height

    #Get the plot area dimensions
    canvas.plot_margin_top = canvas.height / 50
    canvas.plot_margin_x = canvas.width / 10
    canvas.plot_margin_bottom = canvas.height / 10
    canvas.plot_height = canvas.chart_height - (canvas.plot_margin_bottom + canvas.plot_margin_top)
    canvas.plot_width = canvas.chart_width - (2 * canvas.plot_margin_x)

    #Get the top label borders
    canvas.label_canvas.x_start = chart.canvas_margin + (canvas.width / 2)
    canvas.label_canvas.line1_mid = canvas.label_canvas.winfo_height() / 4
    canvas.label_canvas.line1_start = canvas.label_canvas.line1_mid - (canvas.label_canvas.winfo_height() * (1/8))
    canvas.label_canvas.line1_end = canvas.label_canvas.line1_mid + (canvas.label_canvas.winfo_height() * (1/8))
    canvas.label_canvas.line2_mid = canvas.label_canvas.line1_mid + (canvas.label_canvas.winfo_height() / 2)
    canvas.label_canvas.line2_start = canvas.label_canvas.line1_start + (canvas.label_canvas.winfo_height() / 2)
    canvas.label_canvas.line2_end = canvas.label_canvas.line1_end + (canvas.label_canvas.winfo_height() / 2)

    #Get the legend info
    if chart.legend:
        canvas.legend_y_margin = canvas.height / 10
        canvas.legend_x_margin = canvas.legend_width / 10
        canvas.legend_row_height = min(((0.8 * canvas.height) / (len(chart.labels) if len(chart.labels) else 1)), 30)
        canvas.legend_row_width = (canvas.legend_width - (2 * canvas.legend_x_margin))
        canvas.legend_symbol_width = (canvas.legend_row_width * 0.25)
        canvas.legend_text_width = canvas.legend_row_width - canvas.legend_symbol_width


def _chart_write_title(chart, canvas):
    canvas.create_text(
     canvas.chart_width / 2, canvas.title_height / 2,
     text=chart.title,
     width=canvas.chart_width, height=canvas.title_height
    )


def _chart_create_legend(chart, canvas):
    if chart.legend:
        for index, _ in enumerate(chart.labels):
            canvas.create_text(
             canvas.chart_width + canvas.legend_x_margin + canvas.legend_symbol_width + canvas.legend_text_width / 25,
             canvas.legend_y_margin + (canvas.legend_row_height*index) + (canvas.legend_row_height / 2),
             text=chart.labels[index],
             justify=LEFT,
             anchor=W,
             width=canvas.legend_text_width,
             height=canvas.legend_row_height
            )


def _chart_debug_lines(chart, canvas):
    if chart.debug:
        #Title border
        canvas.create_line(
         0, canvas.title_height,
         canvas.chart_width, canvas.title_height,
         dash=(1, 1)
        )

        #Legend border
        canvas.create_line(
         canvas.chart_width, 0,
         canvas.chart_width, canvas.height,
         dash=(1, 1)
        )

        #Plot border
        canvas.create_rectangle(
         canvas.plot_margin_x, canvas.title_height + canvas.plot_margin_top,
         canvas.width - (canvas.legend_width + canvas.plot_margin_x), canvas.height - canvas.plot_margin_bottom,
         dash=(2, 2)
        )

        #Top label
        canvas.label_canvas.create_line(
         canvas.label_canvas.x_start, 0,
         canvas.label_canvas.x_start, canvas.label_canvas.winfo_height(),
         dash=(1,1)
        )
        canvas.label_canvas.create_line(
         canvas.label_canvas.x_start, canvas.label_canvas.line1_start,
         canvas.label_canvas.winfo_width(), canvas.label_canvas.line1_start,
         dash=(1,1)
        )
        canvas.label_canvas.create_line(
         canvas.label_canvas.x_start, canvas.label_canvas.line1_end,
         canvas.label_canvas.winfo_width(), canvas.label_canvas.line1_end,
         dash=(1,1)
        )
        canvas.label_canvas.create_line(
         canvas.label_canvas.x_start, canvas.label_canvas.line2_start,
         canvas.label_canvas.winfo_width(), canvas.label_canvas.line2_start,
         dash=(1,1)
        )
        canvas.label_canvas.create_line(
         canvas.label_canvas.x_start, canvas.label_canvas.line2_end,
         canvas.label_canvas.winfo_width(), canvas.label_canvas.line2_end,
         dash=(1,1)
        )

        #Legend borders
        if chart.legend:
            canvas.create_rectangle(
             canvas.chart_width + canvas.legend_x_margin, canvas.legend_y_margin,
             canvas.width - canvas.legend_x_margin, canvas.height - canvas.legend_y_margin,
             dash=(2,2)
            )
            for index, label in enumerate(chart.labels, start=1):
                canvas.create_line(
                 canvas.chart_width + canvas.legend_x_margin,
                 canvas.legend_y_margin + (index * canvas.legend_row_height),
                 canvas.width - canvas.legend_x_margin,
                 canvas.legend_y_margin + (index * canvas.legend_row_height),
                 dash=(3,3)
                )
            canvas.create_line(
             canvas.chart_width + canvas.legend_x_margin + canvas.legend_symbol_width,
             canvas.legend_y_margin,
             canvas.chart_width + canvas.legend_x_margin + canvas.legend_symbol_width,
             canvas.height - canvas.legend_y_margin,
             dash=(3,3)
            )



#Pie methods
def _pie_prepare_canvas(chart, canvas):
    super(chart.__class__, chart)._prepare_canvas(canvas)

    canvas.radius = min([canvas.plot_width, canvas.plot_height])
    if canvas.radius > 0:
        canvas.x_start = canvas.plot_margin_x + ((canvas.plot_width - canvas.radius) / 2)
        canvas.x_end = (canvas.chart_width - canvas.plot_margin_x) - ((canvas.plot_width - canvas.radius) / 2)
        canvas.y_start = canvas.title_height + canvas.plot_margin_top + ((canvas.plot_height - canvas.radius) / 2)
        canvas.y_end = canvas.height - canvas.plot_margin_bottom - ((canvas.plot_height - canvas.radius) / 2)


def _pie_paint_series(chart, canvas):
    if canvas.radius > 0:
        data_sum = sum(chart.data)
        starts = [360 - ((sum(chart.data[:i])/data_sum)*360) + 90
         for i,_ in enumerate(chart.data, start=1)]
        extents = [(d/data_sum)*360 for d in chart.data]

        for index, _ in enumerate(chart.data):
            canvas.create_arc(
             canvas.x_start,
             canvas.y_start,
             canvas.x_end,
             canvas.y_end,
             start=starts[index],
             extent=extents[index],
             width=1,
             fill=chart.colors[index],
             outline=chart.colors[index]
            )


def _pie_create_legend(chart, canvas):
    super(chart.__class__, chart)._create_legend(canvas)
    if chart.legend:
        for index, _ in enumerate(chart.data):
            canvas.create_rectangle(
             (canvas.width - canvas.legend_width) + canvas.legend_x_margin + (canvas.legend_symbol_width / 10),
             canvas.legend_y_margin + (canvas.legend_row_height*index) + (canvas.legend_row_height / 10),
             (canvas.width - canvas.legend_width) + canvas.legend_x_margin + (canvas.legend_symbol_width - (canvas.legend_symbol_width / 10)),
             canvas.legend_y_margin + (canvas.legend_row_height*(index+1)) - (canvas.legend_row_height / 10),
             fill=chart.colors[index],
             outline=chart.colors[index]
            )


def _pie_debug_lines(chart, canvas):
    super(chart.__class__, chart)._debug_lines(canvas)
    if chart.debug:
        canvas.create_rectangle(canvas.x_start, canvas.y_start,
         canvas.x_end, canvas.y_end, dash=(1,2))



#Axis methods
def _axis_prepare_canvas(chart, canvas):
    super(chart.__class__, chart)._prepare_canvas(canvas)

    canvas.x_tick_length = canvas.plot_margin_bottom / 3
    canvas.x_tick_label_length = canvas.plot_margin_bottom / 4
    canvas.x_axis_label_length = canvas.plot_margin_bottom / 3
    canvas.y_tick_length = canvas.plot_margin_x / 4
    canvas.y_tick_label_length = canvas.plot_margin_x / 2
    canvas.y_axis_label_length = canvas.plot_margin_x / 4


def _axis_draw_grids(chart, canvas):
    if chart.grid:
        for tick in chart.x_ticks:
            if tick >= chart.x_limit[0] and tick <= chart.x_limit[1]:
                canvas.create_line(
                 _get_x_position(chart, canvas, tick), canvas.height - canvas.plot_margin_bottom,
                 _get_x_position(chart, canvas, tick), canvas.title_height + canvas.plot_margin_top,
                 dash=(2,2)
                )

        for tick in chart.y_ticks:
            if tick >= chart.y_limit[0] and tick <= chart.y_limit[1]:
                canvas.create_line(
                 canvas.plot_margin_x, _get_y_position(chart, canvas, tick),
                 canvas.chart_width - canvas.plot_margin_x, _get_y_position(chart, canvas, tick),
                 dash=(2,2)
                )


def _axis_draw_plot_bounds(chart, canvas):
    #Splash some white paint around
    canvas.create_rectangle(
     0, 0,
     canvas.width, canvas.title_height + canvas.plot_margin_top,
     fill="#FFFFFF",
     width=0
    )
    canvas.create_rectangle(
     0, canvas.height - canvas.plot_margin_bottom,
     canvas.width, canvas.height,
     fill="#FFFFFF",
     width=0
    )
    canvas.create_rectangle(
     0, 0,
     canvas.plot_margin_x, canvas.height,
     fill="#FFFFFF",
     width=0
    )
    canvas.create_rectangle(
     canvas.width - (canvas.legend_width + canvas.plot_margin_x), 0,
     canvas.width, canvas.height,
     fill="#FFFFFF",
     width=0
    )

    if canvas.plot_width > 0 and canvas.plot_height > 0:
        #Plot bounds
        canvas.create_rectangle(
         canvas.plot_margin_x,
         canvas.title_height + canvas.plot_margin_top,
         canvas.chart_width - canvas.plot_margin_x,
         canvas.height - canvas.plot_margin_bottom
        )

        #Ticks
        x_font_size = canvas.get_font_size(sorted([t for t in chart.x_tick_labels], key=lambda k: len(k))[-1], height=canvas.x_tick_label_length)
        for index, tick in enumerate(chart.x_ticks):
            if tick >= chart.x_limit[0] and tick <= chart.x_limit[1]:
                canvas.create_line(
                 _get_x_position(chart, canvas, tick), canvas.height - canvas.plot_margin_bottom,
                 _get_x_position(chart, canvas, tick), (canvas.height - canvas.plot_margin_bottom) + (canvas.x_tick_length * 0.8)
                )
                canvas.create_text(
                 _get_x_position(chart, canvas, tick),
                 canvas.height - (canvas.x_axis_label_length + (canvas.x_tick_label_length / 2)),
                 text=chart.x_tick_labels[index],
                 font="Tahoma %i" % x_font_size
                )
        y_font_size = canvas.get_font_size(sorted([t for t in chart.y_tick_labels], key=lambda k: len(k))[-1], width=canvas.y_tick_label_length)
        for index, tick in enumerate(chart.y_ticks):
            if tick >= chart.y_limit[0] and tick <= chart.y_limit[1]:
                canvas.create_line(
                 canvas.plot_margin_x, _get_y_position(chart, canvas, tick),
                 canvas.plot_margin_x - (0.8 * canvas.y_tick_length), _get_y_position(chart, canvas, tick)
                )
                canvas.create_text(
                 canvas.y_axis_label_length + canvas.y_tick_label_length,
                 _get_y_position(chart, canvas, tick),
                 text=chart.y_tick_labels[index],
                 font="Tahoma %i" % y_font_size,
                 justify=RIGHT,
                 anchor=E
                )
        #Axis labels
        canvas.create_text(
         canvas.plot_margin_x + (canvas.plot_width / 2),
         canvas.height - (canvas.x_axis_label_length / 2),
         text=chart.x_label,
         height=canvas.x_axis_label_length * 0.75
        )


def _axis_debug_lines(chart, canvas):
    super(chart.__class__, chart)._debug_lines(canvas)
    if chart.debug:
        canvas.create_line(
         canvas.plot_margin_x - canvas.x_tick_length, canvas.title_height + canvas.plot_margin_top,
         canvas.plot_margin_x - canvas.x_tick_length, canvas.height - (canvas.x_tick_label_length + canvas.x_axis_label_length),
         canvas.chart_width - canvas.plot_margin_x, canvas.height - (canvas.x_tick_label_length + canvas.x_axis_label_length),
         dash=(1,1)
        )
        canvas.create_line(
         canvas.y_axis_label_length, canvas.title_height + canvas.plot_margin_top,
         canvas.y_axis_label_length, canvas.height - canvas.x_axis_label_length,
         canvas.chart_width - canvas.plot_margin_x, canvas.height - canvas.x_axis_label_length,
         dash=(1,1)
        )





def _get_x_position(chart, canvas, value):
    x_distance = chart.x_limit[1] - chart.x_limit[0]
    val_distance = value - chart.x_limit[0]
    return canvas.plot_margin_x + ((val_distance / x_distance) * canvas.plot_width)


def _get_y_position(chart, canvas, value):
    y_distance = chart.y_limit[1] - chart.y_limit[0]
    val_distance = value - chart.y_limit[0]
    return canvas.height - (canvas.plot_margin_bottom + ((val_distance / y_distance) * canvas.plot_height))


def _get_x_value(chart, canvas, position):
    x_proportion = (position - (canvas.plot_margin_x + 1)) / canvas.plot_width
    x_distance = chart.x_limit[1] - chart.x_limit[0]
    value = (x_proportion * x_distance) + chart.x_limit[0]

    if isinstance(chart.x_limit[0], DatetimeDatum):
        return str(datetime.datetime.fromtimestamp(value))
    else:
        return str(value).rstrip("0").rstrip(".")


def _get_y_value(chart, canvas, position):
    y_proportion = ((canvas.height - (canvas.plot_margin_bottom - 1)) - position) / canvas.plot_height
    print(y_proportion)
    y_distance = chart.y_limit[1] - chart.y_limit[0]
    value = (y_proportion * y_distance) + chart.y_limit[0]
    return str(value).rstrip("0").rstrip(".")
