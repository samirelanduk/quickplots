from unittest import TestCase
from quickplots.quick import line
from quickplots.charts import AxisChart

class LineChartCreationTests(TestCase):

    def test_can_create_line_chart(self):
        chart = line((1, 1), (2, 4), (3, 9))
        self.assertIsInstance(chart, AxisChart)


    def test_can_create_line_chart_with_line_properties(self):
        chart = line((1, 1), (2, 4), (3, 9), color="#000099", linestyle="--")
        self.assertEqual(chart.series().color(), "#000099")
        self.assertEqual(chart.series().linestyle(), "--")
