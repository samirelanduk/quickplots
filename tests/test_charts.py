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



class ChartPropertiesTests(TestCase):

    def test_basic_properties(self):
        chart = Chart(title="Title", width=50, height=30)
        self.assertIs(chart.title(), chart._title)
        self.assertIs(chart.width(), chart._width)
        self.assertIs(chart.height(), chart._height)


    def test_can_update_title(self):
        chart = Chart(title="Title", width=50, height=30)
        chart.title("New Title")
        self.assertEqual(chart.title(), "New Title")


    def test_set_title_must_be_str(self):
        chart = Chart(title="Title", width=50, height=30)
        with self.assertRaises(TypeError):
            chart.title(100)
