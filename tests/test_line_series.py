from unittest import TestCase
from unittest.mock import patch
from quickplots.series import LineSeries, Series

class LineSeriesCreationTests(TestCase):

    def test_can_create_line_series(self):
        series = LineSeries((1, 1), (2, 4), (3, 9))
        self.assertIsInstance(series, Series)


    @patch("quickplots.series.Series.__init__")
    def test_axis_chart_uses_chart_initialisation(self, mock):
        series = LineSeries((1, 1), (2, 4), (3, 9))
        self.assertTrue(mock.called)
