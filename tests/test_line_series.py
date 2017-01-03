from unittest import TestCase
from unittest.mock import patch
from quickplots.series import LineSeries, Series

class LineSeriesCreationTests(TestCase):

    def test_can_create_line_series(self):
        series = LineSeries((1, 1), (2, 4), (3, 9))
        self.assertIsInstance(series, Series)
        self.assertEqual(series._color, "#000000")
        self.assertEqual(series._linestyle, "-")


    @patch("quickplots.series.Series.__init__")
    def test_axis_chart_uses_chart_initialisation(self, mock):
        series = LineSeries((1, 1), (2, 4), (3, 9))
        self.assertTrue(mock.called)


    def test_can_create_line_series_with_color(self):
        series = LineSeries((1, 1), (2, 4), (3, 9), color="#FF0000")
        self.assertEqual(series._color, "#FF0000")


    def test_color_must_be_str(self):
        with self.assertRaises(TypeError):
            LineSeries((1, 1), (2, 4), (3, 9), color=100)


    def test_can_create_line_series_with_linestyle(self):
        series = LineSeries((1, 1), (2, 4), (3, 9), linestyle="--")
        self.assertEqual(series._linestyle, "--")


    def test_linestyle_must_be_str(self):
        with self.assertRaises(TypeError):
            LineSeries((1, 1), (2, 4), (3, 9), linestyle=100)


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


    def test_can_modify_color(self):
        series = LineSeries((1, 1), (2, 4), (3, 9))
        series.color("#00FF00")
        self.assertEqual(series.color(), "#00FF00")


    def test_set_color_must_be_str(self):
        series = LineSeries((1, 1), (2, 4), (3, 9))
        with self.assertRaises(TypeError):
            series.color(100)


    def test_can_modify_linestyle(self):
        series = LineSeries((1, 1), (2, 4), (3, 9))
        series.linestyle("--")
        self.assertEqual(series.linestyle(), "--")


    def test_set_linestyle_must_be_str(self):
        series = LineSeries((1, 1), (2, 4), (3, 9))
        with self.assertRaises(TypeError):
            series.linestyle(100)
