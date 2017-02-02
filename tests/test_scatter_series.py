from unittest import TestCase
from unittest.mock import patch
from quickplots.charts import AxisChart
from quickplots.series import ScatterSeries, Series
from omnicanvas import Canvas
from omnicanvas.graphics import Oval

class ScatterSeriesCreationTests(TestCase):

    def test_can_create_scatter_series(self):
        series = ScatterSeries((1, 1), (2, 4), (3, 9))
        self.assertIsInstance(series, Series)
        self.assertEqual(series._size, 5)
        self.assertEqual(series._linewidth, 1)


    @patch("quickplots.series.Series.__init__")
    def test_scatter_chart_uses_chart_initialisation(self, mock):
        series = ScatterSeries((1, 1), (2, 4), (3, 9))
        self.assertTrue(mock.called)


    def test_can_create_scatter_series_with_size(self):
        series = ScatterSeries((1, 1), (2, 4), (3, 9), size=4)
        self.assertEqual(series._size, 4)


    def test_size_must_be_number(self):
        with self.assertRaises(TypeError):
            ScatterSeries((1, 1), (2, 4), (3, 9), size="100")


    def test_can_create_scatter_series_with_linewidth(self):
        series = ScatterSeries((1, 1), (2, 4), (3, 9), linewidth=4)
        self.assertEqual(series._linewidth, 4)


    def test_linewidth_must_be_number(self):
        with self.assertRaises(TypeError):
            ScatterSeries((1, 1), (2, 4), (3, 9), linewidth="100")


    def test_scatter_series_repr(self):
        series = ScatterSeries((1, 1), (2, 4), (3, 9))
        self.assertEqual(str(series), "<ScatterSeries (3 data points)>")
        series = ScatterSeries((1, 1), (2, 4), (3, 9), name="line")
        self.assertEqual(str(series), "<ScatterSeries 'line' (3 data points)>")



class ScatterSeriesPropertyTests(TestCase):

    def test_scatter_line_series_properties(self):
        series = ScatterSeries((1, 1), (2, 4), (3, 9))
        self.assertIs(series._size, series.size())
        self.assertIs(series._linewidth, series.linewidth())


    def test_can_modify_size(self):
        series = ScatterSeries((1, 1), (2, 4), (3, 9))
        series.size(4)
        self.assertEqual(series.size(), 4)


    def test_set_size_must_be_str(self):
        series = ScatterSeries((1, 1), (2, 4), (3, 9))
        with self.assertRaises(TypeError):
            series.size("100")


    def test_can_modify_linewidth(self):
        series = ScatterSeries((1, 1), (2, 4), (3, 9))
        series.linewidth(4)
        self.assertEqual(series.linewidth(), 4)


    def test_set_linewidth_must_be_number(self):
        series = ScatterSeries((1, 1), (2, 4), (3, 9))
        with self.assertRaises(TypeError):
            series.linewidth("100")



class ScatterSeriesPaintingTests(TestCase):

    def setUp(self):
        x = list(range(1, 6))
        y = [n ** 2 for n in x]
        data = list(zip(x, y))
        self.series = ScatterSeries(*data)
        self.chart = AxisChart(self.series)
        self.canvas = Canvas(self.chart.width(), self.chart.height())


    def test_can_write_object_to_canvas(self):
        self.series.write_to_canvas(self.canvas, "series1")
        self.assertEqual(len(self.canvas.graphics()), 5)
        for graphic in self.canvas.graphics():
            self.assertIsInstance(graphic, Oval)


    def test_scatter_series_puts_points_in_correct_place(self):
        self.series.write_to_canvas(self.canvas, "series1")
        markers = [g for g in self.canvas.graphics() if g.name() == "series1"]
        points = self.series.canvas_points()
        self.assertEqual(len(points), len(points))
        for index, point in enumerate(points):
            self.assertEqual(point, (markers[index].center()))


    def test_scatter_series_can_transfer_color(self):
        self.series.color("#DDDDDD")
        self.series.write_to_canvas(self.canvas, "series1")
        markers = [g for g in self.canvas.graphics() if g.name() == "series1"]
        for marker in markers:
            self.assertEqual(marker.fill_color(), "#DDDDDD")


    def test_scatter_series_can_transfer_size(self):
        self.series.size(20)
        self.series.write_to_canvas(self.canvas, "series1")
        markers = [g for g in self.canvas.graphics() if g.name() == "series1"]
        for marker in markers:
            self.assertEqual(marker.width(), 20)


    def test_scatter_series_can_transfer_linewidth(self):
        self.series.linewidth(4)
        self.series.write_to_canvas(self.canvas, "series1")
        markers = [g for g in self.canvas.graphics() if g.name() == "series1"]
        for marker in markers:
            self.assertEqual(marker.line_width(), 4)
