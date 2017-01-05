from .series import LineSeries
from .charts import AxisChart

def line(*args):
    series = LineSeries(*args)
    chart = AxisChart(series)
    return chart
