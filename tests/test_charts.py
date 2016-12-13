from unittest import TestCase
from quickplots.charts import Chart

class ChartCreationTests(TestCase):

    def test_can_create_chart(self):
        chart = Chart()
        self.assertEqual(chart._title, "")


    def test_can_create_chart_with_title(self):
        chart = Chart(title="Chart Title")
        self.assertEqual(chart._title, "Chart Title")
