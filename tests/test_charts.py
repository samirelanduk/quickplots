from unittest import TestCase
from quickplots.charts import Chart
from omnicanvas import Canvas
from omnicanvas.graphics import Text

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


    def test_can_update_width(self):
        chart = Chart(title="Title", width=50, height=30)
        chart.width(1000)
        self.assertEqual(chart.width(), 1000)


    def test_set_width_must_be_numeric(self):
        chart = Chart(title="Title", width=50, height=30)
        with self.assertRaises(TypeError):
            chart.width("100")
        chart.width(100.5)


    def test_can_update_height(self):
        chart = Chart(title="Title", width=50, height=30)
        chart.height(1000)
        self.assertEqual(chart.height(), 1000)


    def test_set_height_must_be_numeric(self):
        chart = Chart(title="Title", width=50, height=30)
        with self.assertRaises(TypeError):
            chart.height("100")
        chart.height(100.5)



class CanvasTests(TestCase):

    def setUp(self):
        self.chart = Chart(title="Title", width=50, height=30)


    def test_chart_can_create_canvas(self):
        canvas = self.chart.create()
        self.assertIsInstance(canvas, Canvas)


    def test_canvas_dimensions_match_chart(self):
        canvas = self.chart.create()
        self.assertEqual(canvas.width(), self.chart.width())
        self.assertEqual(canvas.height(), self.chart.height())


    def test_canvas_has_title(self):
        canvas = self.chart.create()
        title = canvas.get_graphic_by_name("title")
        self.assertIsInstance(title, Text)
        self.assertEqual(title.text(), self.chart.title())


    def test_title_is_centered_properly(self):
        canvas = self.chart.create()
        title = canvas.get_graphic_by_name("title")
        self.assertEqual(title.x(), self.chart.width() / 2)
        self.assertEqual(title.vertical_align(), "bottom")
