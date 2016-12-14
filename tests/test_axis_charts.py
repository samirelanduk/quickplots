from unittest import TestCase
from quickplots.charts import AxisChart, Chart

class ChartCreationTests(TestCase):

    def test_can_create_chart(self):
        chart = AxisChart()
        self.assertIsInstance(chart, Chart)
