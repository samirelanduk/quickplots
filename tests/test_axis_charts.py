from unittest import TestCase
from unittest.mock import patch
from quickplots.charts import AxisChart, Chart
from omnicanvas import Canvas
from omnicanvas.graphics import Text, Rectangle

class AxisChartCreationTests(TestCase):

    def test_can_create_axis_chart(self):
        chart = AxisChart()
        self.assertIsInstance(chart, Chart)
        self.assertEqual(chart._x_label, "")
        self.assertEqual(chart._y_label, "")
        self.assertEqual(chart._all_series, [])
        self.assertEqual(chart._horizontal_padding, 0.1)
        self.assertEqual(chart._vertical_padding, 0.1)


    @patch("quickplots.charts.Chart.__init__")
    def test_axis_chart_uses_chart_initialisation(self, mock):
        chart = AxisChart()
        self.assertTrue(mock.called)


    def test_can_create_axis_chart_with_axis_labels(self):
        chart = AxisChart(x_label="Input")
        self.assertEqual(chart._x_label, "Input")
        chart = AxisChart(y_label="Output")
        self.assertEqual(chart._y_label, "Output")


    def test_axis_labels_must_be_string(self):
        with self.assertRaises(TypeError):
            AxisChart(x_label=1)
        with self.assertRaises(TypeError):
            AxisChart(y_label=1)


    def test_repr(self):
        chart = AxisChart()
        self.assertEqual(str(chart), "<AxisChart (0 series)>")
        chart._all_series.append("dummy series")
        self.assertEqual(str(chart), "<AxisChart (1 series)>")



class AxisChartPropertyTests(TestCase):

    def test_basic_properties(self):
        chart = AxisChart()
        self.assertEqual(chart.horizontal_padding(), chart._horizontal_padding)
        self.assertEqual(chart.vertical_padding(), chart._vertical_padding)
        self.assertIs(chart.x_label(), chart._x_label)
        self.assertIs(chart.y_label(), chart._y_label)


    def test_can_update_axis_labels(self):
        chart = AxisChart()
        chart.x_label("Input")
        self.assertEqual(chart.x_label(), "Input")
        chart.y_label("Output")
        self.assertEqual(chart.y_label(), "Output")


    def test_set_axis_labels_must_be_str(self):
        chart = AxisChart()
        with self.assertRaises(TypeError):
            chart.x_label(1)
        with self.assertRaises(TypeError):
            chart.y_label(1)


    def test_can_update_padding(self):
        chart = AxisChart()
        chart.horizontal_padding(0.4)
        self.assertEqual(chart.horizontal_padding(), 0.4)
        chart.vertical_padding(0.3)
        self.assertEqual(chart.vertical_padding(), 0.3)


    def test_padding_must_be_float(self):
        chart = AxisChart()
        with self.assertRaises(TypeError):
            chart.horizontal_padding(10)
        with self.assertRaises(TypeError):
            chart.vertical_padding(10)


    def test_padding_must_be_between_0_and_half(self):
        chart = AxisChart()
        with self.assertRaises(ValueError):
            chart.horizontal_padding(0.0)
        with self.assertRaises(ValueError):
            chart.vertical_padding(0.5)



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


    def test_axes_respect_padding(self):
        canvas = self.chart.create()
        axes = canvas.get_graphic_by_name("axes")
        self.assertEqual(axes.x(), 70)
        self.assertEqual(axes.y(), 50)
        self.assertEqual(axes.width(), 560)
        self.assertEqual(axes.height(), 400)
        self.chart.horizontal_padding(0.4)
        self.chart.vertical_padding(0.01)
        canvas = self.chart.create()
        axes = canvas.get_graphic_by_name("axes")
        self.assertEqual(axes.x(), 280)
        self.assertEqual(axes.y(), 5)
        self.assertEqual(axes.width(), 140)
        self.assertEqual(axes.height(), 490)
        canvas.save("temp.svg")


    def test_axes_have_transparent_interior(self):
        canvas = self.chart.create()
        axes = canvas.get_graphic_by_name("axes")
        self.assertEqual(axes.opacity(), 0)
