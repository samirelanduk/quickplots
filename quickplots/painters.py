def _empty(chart):
    pass


def _chart_prepare_canvas(chart):
    canvas = chart.canvas
    canvas.graphics = []

    #Get the chart area dimensions
    canvas.title_height = canvas.height / 10
    canvas.legend_width = canvas.width / 4 if chart.legend else 0
    canvas.chart_width = canvas.width - canvas.legend_width
    canvas.chart_height = canvas.height - canvas.title_height

    #Get the plot area dimensions
    canvas.plot_margin_top = canvas.height / 50
    canvas.plot_margin_left = canvas.width / 10
    canvas.plot_margin_right = canvas.width / 20
    canvas.plot_margin_bottom = canvas.height / 10
    canvas.plot_height = canvas.chart_height - (
     canvas.plot_margin_bottom + canvas.plot_margin_top)
    canvas.plot_width = canvas.chart_width - (
     canvas.plot_margin_left + canvas.plot_margin_right)

    #Get the legend info
    if chart.legend:
        canvas.legend_y_margin = canvas.height / 10
        canvas.legend_x_margin = canvas.legend_width / 10
        canvas.legend_row_height = min(
         ((canvas.height - (2 * canvas.legend_y_margin)) / (
          len(chart.legend_labels) if len(chart.legend_labels) else 1)),
          30
         )
        canvas.legend_row_width = (canvas.legend_width - (
         2 * canvas.legend_x_margin))
        canvas.legend_symbol_width = (canvas.legend_row_width * 0.25)
        canvas.legend_text_width = canvas.legend_row_width - canvas.legend_symbol_width
    canvas.legend_symbols = 0


def _chart_write_title(chart):
    canvas = chart.canvas
    canvas.create_text(
     0,
     0,
     canvas.width - canvas.legend_width,
     canvas.title_height,
     text=chart.title,
     max_font_size=32
    )


def _chart_write_legend_labels(chart):
    canvas = chart.canvas
    if chart.legend:
        for index, _ in enumerate(chart.legend_labels):
            canvas.create_text(
             canvas.chart_width + canvas.legend_x_margin +\
              canvas.legend_symbol_width + (canvas.legend_text_width / 25),
             canvas.legend_y_margin + (canvas.legend_row_height*index) + (
              canvas.legend_row_height / 2),
             canvas.legend_text_width * (24/25),
             canvas.legend_row_height,
             text=chart.legend_labels[index],
             max_font_size=18
            )


def _chart_debug_lines(chart):
    canvas = chart.canvas
    if chart.debug:
        #Title border
        canvas.create_line(
         0, canvas.title_height,
         canvas.chart_width, canvas.title_height,
         style="."
        )

        #Legend border
        canvas.create_line(
         canvas.chart_width, 0,
         canvas.chart_width, canvas.height,
         style="."
        )

        #Plot border
        canvas.create_rectangle(
         canvas.plot_margin_left,
         canvas.title_height + canvas.plot_margin_top,
         canvas.width - (canvas.legend_width + canvas.plot_margin_right),
         canvas.height - canvas.plot_margin_bottom,
         line_style="--"
        )

        #Legend borders
        if chart.legend:
            canvas.create_rectangle(
             canvas.chart_width + canvas.legend_x_margin,
             canvas.legend_y_margin,
             canvas.width - canvas.legend_x_margin,
             canvas.height - canvas.legend_y_margin,
             line_style="--"
            )
            for index, label in enumerate(chart.legend_labels, start=1):
                canvas.create_line(
                 canvas.chart_width + canvas.legend_x_margin,
                 canvas.legend_y_margin + (index * canvas.legend_row_height),
                 canvas.width - canvas.legend_x_margin,
                 canvas.legend_y_margin + (index * canvas.legend_row_height),
                 style="--"
                )
            canvas.create_line(
             canvas.chart_width + canvas.legend_x_margin + canvas.legend_symbol_width,
             canvas.legend_y_margin,
             canvas.chart_width + canvas.legend_x_margin + canvas.legend_symbol_width,
             canvas.height - canvas.legend_y_margin,
             style="--"
            )
