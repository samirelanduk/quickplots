def empty(chart):
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
