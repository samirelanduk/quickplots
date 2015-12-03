from tkinter import *


class Chart:
    """Something with a window representation and a single canvas"""

    def __init__(self, title="", legend=False, window_dimensions=[900, 700],
     window_title="", background_color="#CCCCCC", canvas_margin=50, debug=False):
        self.title = title
        self.legend = legend
        self.window_dimensions = window_dimensions
        self.window_title = window_title
        self.background_color = background_color
        self.canvas_margin = canvas_margin
        self.debug = debug


    def show(self):
        root = Tk()
        root.title(self.window_title)
        root.geometry("%ix%i" % (self.window_dimensions[0], self.window_dimensions[1]))

        root.frame = Frame(root, background=self.background_color)
        root.frame.pack(fill=BOTH, expand=YES)

        root.frame.canvas = ChartCanvas(root.frame, self, background="#FFFFFF")
        root.frame.canvas.pack(fill=BOTH, expand=YES, padx=self.canvas_margin, pady=self.canvas_margin)

        root.mainloop()


    def _prepare_canvas(self, canvas):
        canvas.delete("all")
        #Get the canvas dimensions
        canvas.width = canvas.winfo_width()
        canvas.height = canvas.winfo_height()

        #Get the chart area dimensions
        canvas.title_height = canvas.height / 10
        canvas.legend_width = 200 if self.legend else 0
        canvas.chart_width = canvas.width - canvas.legend_width
        canvas.chart_height = canvas.height - canvas.title_height

        #Get the plot area dimensions
        canvas.plot_margin = max(((canvas.height * canvas.width) / 10000, canvas.width / 20))
        canvas.plot_margin_top = canvas.height / 50
        canvas.plot_height = canvas.chart_height - (canvas.plot_margin + canvas.plot_margin_top)
        canvas.plot_width = canvas.chart_width - (2 * canvas.plot_margin)

        #Get the legend info
        if self.legend:
            canvas.legend_top_margin = 80
            canvas.legend_x_margin = 10
            canvas.legend_row_height = 30
            canvas.legend_padding = 5


    def _debug_lines(self, canvas):
        if self.debug:
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
             canvas.plot_margin, canvas.title_height + canvas.plot_margin_top,
             canvas.width - (canvas.legend_width + canvas.plot_margin), canvas.height - canvas.plot_margin,
             dash=(2, 2)
            )

            #Legend borders
            if self.legend:
                canvas.create_rectangle(
                 canvas.chart_width + canvas.legend_x_margin, canvas.legend_top_margin,
                 canvas.width - canvas.legend_x_margin, canvas.height,
                 dash=(2,2)
                )
                for row in range((canvas.height - canvas.legend_top_margin)
                 // canvas.legend_row_height):
                    canvas.create_line(
                     canvas.chart_width + canvas.legend_x_margin,
                     canvas.legend_top_margin + ((row+1) * canvas.legend_row_height),
                     canvas.width - canvas.legend_x_margin,
                     canvas.legend_top_margin + ((row+1) * canvas.legend_row_height),
                     dash=(3,3)
                    )


    def _write_title(self, canvas):
        canvas.create_text(
         canvas.chart_width / 2, canvas.title_height / 2,
         text=self.title,
         font="bold %i" % (canvas.title_height / 1.5)
        )


    def _paint_series(self, canvas):
        pass


    def _create_legend(self, canvas):
        pass



class ChartCanvas(Canvas):
    """A canvas that has an associated chart, and knows how to draw that chart"""

    def __init__(self, master, chart, **kwargs):
        Canvas.__init__(self, master, **kwargs)
        self.chart = chart
        self.bind("<Configure>", self.request_repaint)


    def request_repaint(self, event):
        self.chart._prepare_canvas(self)
        self.chart._debug_lines(self)
        self.chart._write_title(self)
        self.chart._paint_series(self)
        self.chart._create_legend(self)
