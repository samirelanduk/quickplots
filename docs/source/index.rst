QuickPlots
==========

quickplots is a lightweight, object-oriented plotting library for Python. It
currently supports line charts.

Example
-------

  >>> import quickplots
  >>> chart = quickplots.line((0, 0), (1, 1), (2, 4), (3, 9), name="squares")
  >>> chart.get_series_by_name("squares").color("#FF0000")
  >>> chart.create().save("chart.svg")


Table of Contents
-----------------

.. toctree ::

    installing
    overview
    api
    changelog
