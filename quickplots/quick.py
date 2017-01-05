from .series import LineSeries
from .charts import AxisChart

def line(*args, **kwargs):
    line_series_kwargs = {}
    for kwarg in ("name", "color", "linestyle"):
        if kwarg in kwargs:
            line_series_kwargs[kwarg] = kwargs[kwarg]
            del kwargs[kwarg]
    series = LineSeries(*args, **line_series_kwargs)
    chart = AxisChart(series, **kwargs)
    return chart
