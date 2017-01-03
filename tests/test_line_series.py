from unittest import TestCase
from unittest.mock import patch
from quickplots.series import LineSeries, Series

class LineSeriesCreationTests(TestCase):

    def test_can_create_line_series(self):
        series = LineSeries((1, 1), (2, 4), (3, 9))
        self.assertIsInstance(series, Series)
        self.assertEqual(series._color, "#000000")


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



class LineSeriesPropertyTests(TestCase):

    def test_basic_line_series_properties(self):
        series = LineSeries((1, 1), (2, 4), (3, 9))
        self.assertIs(series._color, series.color())
