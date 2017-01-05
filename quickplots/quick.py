from .series import LineSeries
from .charts import AxisChart

def line(*args, **kwargs):
    series = LineSeries(*args, **kwargs)
    chart = AxisChart(series)
    return chart
