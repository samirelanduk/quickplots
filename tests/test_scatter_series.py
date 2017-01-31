from unittest import TestCase
from unittest.mock import patch
from quickplots.series import ScatterSeries, Series

class ScatterSeriesCreationTests(TestCase):

    def test_can_create_scatter_series(self):
        series = ScatterSeries((1, 1), (2, 4), (3, 9))
        self.assertIsInstance(series, Series)
        self.assertEqual(series._color, "#FF0000")
        self.assertEqual(series._size, 5)
        self.assertEqual(series._linewidth, 1)


    @patch("quickplots.series.Series.__init__")
    def test_scatter_chart_uses_chart_initialisation(self, mock):
        series = ScatterSeries((1, 1), (2, 4), (3, 9))
        self.assertTrue(mock.called)


    def test_can_create_scatter_series_with_color(self):
        series = ScatterSeries((1, 1), (2, 4), (3, 9), color="#FF0000")
        self.assertEqual(series._color, "#FF0000")


    def test_color_must_be_str(self):
        with self.assertRaises(TypeError):
            ScatterSeries((1, 1), (2, 4), (3, 9), color=100)


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
        self.assertIs(series._color, series.color())
        self.assertIs(series._size, series.size())
        self.assertIs(series._linewidth, series.linewidth())


    def test_can_modify_color(self):
        series = ScatterSeries((1, 1), (2, 4), (3, 9))
        series.color("#00FF00")
        self.assertEqual(series.color(), "#00FF00")


    def test_set_color_must_be_str(self):
        series = ScatterSeries((1, 1), (2, 4), (3, 9))
        with self.assertRaises(TypeError):
            series.color(100)


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
