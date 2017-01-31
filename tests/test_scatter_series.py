from unittest import TestCase
from unittest.mock import patch
from quickplots.series import ScatterSeries, Series

class LineSeriesCreationTests(TestCase):

    def test_can_create_line_series(self):
        series = ScatterSeries((1, 1), (2, 4), (3, 9))
        self.assertIsInstance(series, Series)


    @patch("quickplots.series.Series.__init__")
    def test_scatter_chart_uses_chart_initialisation(self, mock):
        series = ScatterSeries((1, 1), (2, 4), (3, 9))
        self.assertTrue(mock.called)


    def test_scatter_series_repr(self):
        series = ScatterSeries((1, 1), (2, 4), (3, 9))
        self.assertEqual(str(series), "<ScatterSeries (3 data points)>")
        series = ScatterSeries((1, 1), (2, 4), (3, 9), name="line")
        self.assertEqual(str(series), "<ScatterSeries 'line' (3 data points)>")
