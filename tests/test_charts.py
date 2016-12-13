from unittest import TestCase
from quickplots.charts import Chart

class ChartCreationTests(TestCase):

    def test_can_create_chart(self):
        chart = Chart()
        self.assertEqual(chart._title, "")
        self.assertEqual(chart._width, 700)
        self.assertEqual(chart._height, 500)


    def test_can_create_chart_with_title(self):
        chart = Chart(title="Chart Title")
        self.assertEqual(chart._title, "Chart Title")


    def test_can_create_chart_with_width(self):
        chart = Chart(width=100)
        self.assertEqual(chart._width, 100)


    def test_can_create_chart_with_height(self):
        chart = Chart(height=100)
        self.assertEqual(chart._height, 100)
