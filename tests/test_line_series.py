from unittest import TestCase
from unittest.mock import patch
from quickplots.series import LineSeries, Series
from quickplots.charts import AxisChart
from omnicanvas import Canvas
from omnicanvas.graphics import Polyline

class LineSeriesCreationTests(TestCase):

    def test_can_create_line_series(self):
        series = LineSeries((1, 1), (2, 4), (3, 9))
        self.assertIsInstance(series, Series)
        self.assertEqual(series._linestyle, "-")
        self.assertEqual(series._linewidth, 2)


    @patch("quickplots.series.Series.__init__")
    def test_line_series_uses_series_initialisation(self, mock):
        series = LineSeries((1, 1), (2, 4), (3, 9))
        self.assertTrue(mock.called)


    def test_can_create_line_series_with_linestyle(self):
        series = LineSeries((1, 1), (2, 4), (3, 9), linestyle="--")
        self.assertEqual(series._linestyle, "--")


    def test_linestyle_must_be_str(self):
        with self.assertRaises(TypeError):
            LineSeries((1, 1), (2, 4), (3, 9), linestyle=100)


    def test_can_create_line_series_with_linewidth(self):
        series = LineSeries((1, 1), (2, 4), (3, 9), linewidth=4)
        self.assertEqual(series._linewidth, 4)


    def test_linewidth_must_be_number(self):
        with self.assertRaises(TypeError):
            LineSeries((1, 1), (2, 4), (3, 9), linewidth="100")


    def test_line_series_repr(self):
        series = LineSeries((1, 1), (2, 4), (3, 9))
        self.assertEqual(str(series), "<LineSeries (3 data points)>")
        series = LineSeries((1, 1), (2, 4), (3, 9), name="line")
        self.assertEqual(str(series), "<LineSeries 'line' (3 data points)>")



class LineSeriesPropertyTests(TestCase):

    def test_basic_line_series_properties(self):
        series = LineSeries((1, 1), (2, 4), (3, 9))
        self.assertIs(series._color, series.color())
        self.assertIs(series._linestyle, series.linestyle())
        self.assertIs(series._linewidth, series.linewidth())


    def test_can_modify_linestyle(self):
        series = LineSeries((1, 1), (2, 4), (3, 9))
        series.linestyle("--")
        self.assertEqual(series.linestyle(), "--")


    def test_set_linestyle_must_be_str(self):
        series = LineSeries((1, 1), (2, 4), (3, 9))
        with self.assertRaises(TypeError):
            series.linestyle(100)


    def test_can_modify_linewidth(self):
        series = LineSeries((1, 1), (2, 4), (3, 9))
        series.linewidth(4)
        self.assertEqual(series.linewidth(), 4)


    def test_set_linewidth_must_be_number(self):
        series = LineSeries((1, 1), (2, 4), (3, 9))
        with self.assertRaises(TypeError):
            series.linewidth("100")



class LineSeriesPaintingTests(TestCase):

    def setUp(self):
        x = list(range(1, 6))
        y = [n ** 2 for n in x]
        data = list(zip(x, y))
        self.series = LineSeries(*data)
        self.chart = AxisChart(self.series)
        self.canvas = Canvas(self.chart.width(), self.chart.height())


    def test_can_write_object_to_canvas(self):
        self.series.write_to_canvas(self.canvas, "series1")
        self.assertEqual(len(self.canvas.graphics()), 1)
        self.assertIsInstance(
         self.canvas.get_graphic_by_name("series1"),
         Polyline
        )


    def test_line_series_puts_points_in_correct_place(self):
        self.series.write_to_canvas(self.canvas, "series1")
        line = self.canvas.get_graphic_by_name("series1")
        points = self.series.canvas_points()
        self.assertEqual(len(points), len(line.coordinates(xy_pairs=True)))
        for index, point in enumerate(points):
            self.assertEqual(point, line.coordinates(xy_pairs=True)[index])


    def test_line_series_can_transfer_color(self):
        self.series.color("#DDDDDD")
        self.series.write_to_canvas(self.canvas, "series1")
        line = self.canvas.get_graphic_by_name("series1")
        self.assertEqual(line.line_color(), "#DDDDDD")


    def test_line_series_can_transfer_line_style(self):
        self.series.linestyle("--")
        self.series.write_to_canvas(self.canvas, "series1")
        line = self.canvas.get_graphic_by_name("series1")
        self.assertEqual(line.line_style(), "--")


    def test_line_series_can_transfer_line_width(self):
        self.series.linewidth(5)
        self.series.write_to_canvas(self.canvas, "series1")
        line = self.canvas.get_graphic_by_name("series1")
        self.assertEqual(line.line_width(), 5)
