Overview
--------

Creating Charts
~~~~~~~~~~~~~~~
The easiest way to create a chart is with the quick single-series functions.
For example, the following code would create a line chart of the sine function:

  >>> import quickplots
  >>> from math import sin, radians
  >>> data = [(x, sin(radians(x))) for x in range(360)]
  >>> chart = quickplots.line(*data, color="#0000FF", title="sin(x)")
  >>> chart.x_label("angle")
  >>> chart.y_label("sine of angle")

A few things to note here. The ``line`` function takes (x, y) data points as its
positional arguments - these can be lists or tuples. All arguments that are not
data must be given as keyword arguments.

As with all other quickplots functions that accept data in this way, you can
also provide the data in the form of two lists (or tuples) - one of all the x
values and one of all the y values:

  >>> chart = quickplots.line([x for x in range(360)], [sin(radians(x)) for x in range(360)])

Line charts
###########

Use the ``line`` function as above to create line charts. You can pass in hex
colors to the ``color`` function and line styles (see the full documentation
for a full list of styles) to the ``linestyle`` argument.

Charts themselves also have a ``line`` method for adding new line series. To
add the cosine function to the above chart, you would do the following:

  >>> cosine_data = [(x, cos(radians(x))) for x in range(360)]
  >>> chart.line(*cosine_data, color="#00FF00")

Modifying Charts
~~~~~~~~~~~~~~~~

Charts have a title, an x axis label, and a y axis label, which can be modified
like so:

  >>> chart.title()
  'sin(x)'
  >>> chart.title("A new title")
  >>> chart.title()
  'A new title'
  >>> chart.x_label("A new x-axis label")
  >>> chart.y_label("A new y-axis label")

Charts can have one or more Series objects. The ``series`` property will return
the first series, and the ``all_series()`` will return all the series on the
chart.

Outputting Charts
~~~~~~~~~~~~~~~~~

All charts have a ``create`` method which will create an OmniCanvas canvas with
the chart painted to it. These can be saved or rendered as SVG text.

  >>> chart.create()
  <Canvas 700×500 (7 Graphics)>
  >>> chart.create().save("Charts.svg")
