from unittest import TestCase
from unittest.mock import patch, Mock
from quickplots.charts import AxisChart, Chart
from quickplots.series import Series
from omnicanvas import Canvas
from omnicanvas.graphics import Text, Rectangle

class AxisChartTest(TestCase):

    def setUp(self):
        self.series1 = Mock(Series)
        self.series1.name.return_value = "series1"
        self.series2 = Mock(Series)
        self.series2.name.return_value = "series2"
        self.series3 = Mock(Series)
        self.series3.name.return_value = "series3"


class AxisChartCreationTests(AxisChartTest):

    def test_can_create_axis_chart(self):
        chart = AxisChart(self.series1)
        self.assertIsInstance(chart, Chart)
        self.assertEqual(chart._all_series, [self.series1])
        self.assertEqual(chart._x_label, "")
        self.assertEqual(chart._y_label, "")
        self.assertEqual(chart._horizontal_padding, 0.1)
        self.assertEqual(chart._vertical_padding, 0.1)


    @patch("quickplots.charts.Chart.__init__")
    def test_axis_chart_uses_chart_initialisation(self, mock):
        chart = AxisChart(self.series1)
        self.assertTrue(mock.called)


    def test_can_create_axis_chart_with_multiple_series(self):
        chart = AxisChart(self.series1, self.series2, self.series3)
        self.assertEqual(
         chart._all_series,
         [self.series1, self.series2, self.series3]
        )


    def test_axis_chart_series_must_be_of_type_series(self):
        with self.assertRaises(TypeError):
            AxisChart(self.series1, [1, 2, 3])


    def test_axis_chart_requires_at_least_one_series(self):
        with self.assertRaises(ValueError):
            AxisChart()


    def test_can_create_axis_chart_with_axis_labels(self):
        chart = AxisChart(self.series1, x_label="Input")
        self.assertEqual(chart._x_label, "Input")
        chart = AxisChart(self.series1, y_label="Output")
        self.assertEqual(chart._y_label, "Output")


    def test_axis_labels_must_be_string(self):
        with self.assertRaises(TypeError):
            AxisChart(self.series1, x_label=1)
        with self.assertRaises(TypeError):
            AxisChart(self.series1, y_label=1)


    def test_repr(self):
        chart = AxisChart(self.series1)
        self.assertEqual(str(chart), "<AxisChart (1 series)>")
        chart._all_series.append(self.series2)
        self.assertEqual(str(chart), "<AxisChart (2 series)>")



class AxisChartPropertyTests(AxisChartTest):

    def test_basic_properties(self):
        chart = AxisChart(self.series1)
        self.assertEqual(chart.all_series(), chart._all_series)
        self.assertEqual(chart.horizontal_padding(), chart._horizontal_padding)
        self.assertEqual(chart.vertical_padding(), chart._vertical_padding)
        self.assertIs(chart.x_label(), chart._x_label)
        self.assertIs(chart.y_label(), chart._y_label)


    def test_all_series_is_not_directly_modifable(self):
        chart = AxisChart(self.series1)
        chart.all_series().append("Bad series")
        self.assertEqual(chart.all_series(), [self.series1])


    def test_can_update_axis_labels(self):
        chart = AxisChart(self.series1)
        chart.x_label("Input")
        self.assertEqual(chart.x_label(), "Input")
        chart.y_label("Output")
        self.assertEqual(chart.y_label(), "Output")


    def test_set_axis_labels_must_be_str(self):
        chart = AxisChart(self.series1)
        with self.assertRaises(TypeError):
            chart.x_label(1)
        with self.assertRaises(TypeError):
            chart.y_label(1)


    def test_can_update_padding(self):
        chart = AxisChart(self.series1)
        chart.horizontal_padding(0.4)
        self.assertEqual(chart.horizontal_padding(), 0.4)
        chart.vertical_padding(0.3)
        self.assertEqual(chart.vertical_padding(), 0.3)


    def test_padding_must_be_float(self):
        chart = AxisChart(self.series1)
        with self.assertRaises(TypeError):
            chart.horizontal_padding(10)
        with self.assertRaises(TypeError):
            chart.vertical_padding(10)


    def test_padding_must_be_between_0_and_half(self):
        chart = AxisChart(self.series1)
        with self.assertRaises(ValueError):
            chart.horizontal_padding(0.0)
        with self.assertRaises(ValueError):
            chart.vertical_padding(0.5)



class AxisChartSeriesTests(AxisChartTest):

    def test_can_add_series(self):
        chart = AxisChart(self.series1)
        chart.add_series(self.series2)
        self.assertEqual(chart.all_series(), [self.series1, self.series2])
        chart.add_series(self.series3)
        self.assertEqual(
         chart.all_series(),
         [self.series1, self.series2, self.series3]
        )


    def test_can_only_add_series(self):
        chart = AxisChart(self.series1)
        with self.assertRaises(TypeError):
            chart.add_series("Series")


    def test_can_remove_series(self):
        chart = AxisChart(self.series1, self.series2)
        chart.remove_series(self.series1)
        self.assertEqual(chart.all_series(), [self.series2])


    def test_cannot_remove_last_series(self):
        chart = AxisChart(self.series1)
        with self.assertRaises(ValueError):
            chart.remove_series(self.series1)


    def test_can_get_series_by_name(self):
        chart = AxisChart(self.series1, self.series2, self.series3)
        self.assertIs(chart.get_series_by_name("series1"), self.series1)
        self.assertIs(chart.get_series_by_name("series2"), self.series2)
        self.assertIs(chart.get_series_by_name("series3"), self.series3)
        self.assertIs(chart.get_series_by_name("series4"), None)


    def test_can_only_search_series_name_by_str(self):
        chart = AxisChart(self.series1, self.series2, self.series3)
        with self.assertRaises(TypeError):
            chart.get_series_by_name(self.series1)



class AxisChartCanvasTests(AxisChartTest):

    def setUp(self):
        AxisChartTest.setUp(self)
        self.chart = AxisChart(self.series1, title="Test AxisChart")


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


    def test_empty_axis_labels_do_not_have_canvas_text(self):
        canvas = self.chart.create()
        self.assertEqual(canvas.get_graphic_by_name("x_label"), None)
        self.assertEqual(canvas.get_graphic_by_name("y_label"), None)


    def test_axis_labels_do_have_text_on_canvas(self):
        self.chart.x_label("Input")
        self.chart.y_label("Output")
        canvas = self.chart.create()
        x_label = canvas.get_graphic_by_name("x_label")
        y_label = canvas.get_graphic_by_name("y_label")
        self.assertIsInstance(x_label, Text)
        self.assertIsInstance(y_label, Text)
        self.assertEqual(x_label.text(), "Input")
        self.assertEqual(y_label.text(), "Output")


    def test_axis_labels_are_positioned_correctly(self):
        self.chart.x_label("Input")
        self.chart.y_label("Output")
        canvas = self.chart.create()
        x_label = canvas.get_graphic_by_name("x_label")
        y_label = canvas.get_graphic_by_name("y_label")
        self.assertEqual(x_label.x(), 350)
        self.assertEqual(x_label.y(), 475)
        self.assertEqual(y_label.x(), 35)
        self.assertEqual(y_label.y(), 250)
        self.chart.horizontal_padding(0.2)
        self.chart.vertical_padding(0.3)
        canvas.save("temp.svg")
        canvas = self.chart.create()
        x_label = canvas.get_graphic_by_name("x_label")
        y_label = canvas.get_graphic_by_name("y_label")
        self.assertEqual(x_label.x(), 350)
        self.assertEqual(x_label.y(), 425)
        self.assertEqual(y_label.x(), 70)
        self.assertEqual(y_label.y(), 250)


    def test_axis_labels_are_centered(self):
        self.chart.x_label("Input")
        self.chart.y_label("Output")
        canvas = self.chart.create()
        x_label = canvas.get_graphic_by_name("x_label")
        y_label = canvas.get_graphic_by_name("y_label")
        self.assertEqual(x_label.horizontal_align(), "center")
        self.assertEqual(x_label.vertical_align(), "center")
        self.assertEqual(y_label.horizontal_align(), "center")
        self.assertEqual(y_label.vertical_align(), "center")


    def test_y_axis_label_is_rotated(self):
        self.chart.y_label("Output")
        canvas = self.chart.create()
        y_label = canvas.get_graphic_by_name("y_label")
        self.assertEqual(y_label.rotation(), (35, 250, 270))
        self.chart.horizontal_padding(0.2)
        canvas = self.chart.create()
        y_label = canvas.get_graphic_by_name("y_label")
        self.assertEqual(y_label.rotation(), (70, 250, 270))
