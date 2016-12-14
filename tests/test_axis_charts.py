from unittest import TestCase
from unittest.mock import patch
from quickplots.charts import AxisChart, Chart
from omnicanvas import Canvas
from omnicanvas.graphics import Text, Rectangle

class ChartCreationTests(TestCase):

    def test_can_create_axis_chart(self):
        chart = AxisChart()
        self.assertIsInstance(chart, Chart)
        self.assertEqual(chart._all_series, [])


    @patch("quickplots.charts.Chart.__init__")
    def test_axis_chart_uses_chart_initialisation(self, mock):
        chart = AxisChart()
        self.assertTrue(mock.called)


    def test_repr(self):
        chart = AxisChart()
        self.assertEqual(str(chart), "<AxisChart (0 series)>")
        chart._all_series.append("dummy series")
        self.assertEqual(str(chart), "<AxisChart (1 series)>")



class AxisChartCanvasTests(TestCase):

    def setUp(self):
        self.chart = AxisChart(title="Test AxisChart")


    def test_can_create_basic_canvas(self):
        canvas = self.chart.create()
        title = canvas.get_graphic_by_name("title")
        self.assertEqual(title.text(), "Test AxisChart")


    def test_chart_has_axes(self):
        canvas = self.chart.create()
        axes = canvas.get_graphic_by_name("axes")
        self.assertIsInstance(axes, Rectangle)
