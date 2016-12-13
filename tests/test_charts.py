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


    def test_title_must_be_str(self):
        with self.assertRaises(TypeError):
            Chart(title=100)


    def test_can_create_chart_with_width(self):
        chart = Chart(width=100)
        self.assertEqual(chart._width, 100)


    def test_width_must_be_numeric(self):
        with self.assertRaises(TypeError):
            Chart(width="100")
        Chart(width=100.6)


    def test_can_create_chart_with_height(self):
        chart = Chart(height=100)
        self.assertEqual(chart._height, 100)


    def test_height_must_be_numeric(self):
        with self.assertRaises(TypeError):
            Chart(height="100")
        Chart(height=100.6)


    def test_chart_repr(self):
        chart = Chart(title="Title", width=50, height=30)
        self.assertEqual(str(chart), "<Chart (50×30)>")
