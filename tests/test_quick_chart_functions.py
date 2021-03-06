from unittest import TestCase
from omnicanvas import colors
from quickplots.quick import line, scatter
from quickplots.charts import AxisChart

class LineChartCreationTests(TestCase):

    def test_can_create_line_chart(self):
        chart = line((1, 1), (2, 4), (3, 9))
        self.assertIsInstance(chart, AxisChart)


    def test_default_line_color_is_first_omnicanvas_color(self):
        chart = line((1, 1), (2, 4), (3, 9))
        self.assertEqual(chart.series().color(), colors[0])


    def test_can_create_line_chart_with_line_properties(self):
        chart = line(
         (1, 1), (2, 4), (3, 9),
         name="squares", color="#000099", linestyle="--", linewidth=10,
        )
        self.assertEqual(chart.series().name(), "squares")
        self.assertEqual(chart.series().color(), "#000099")
        self.assertEqual(chart.series().linestyle(), "--")
        self.assertEqual(chart.series().linewidth(), 10)


    def test_can_create_line_chart_with_chart_properties(self):
        chart = line(
         (1, 1), (2, 4), (3, 9),
         name="squares", color="#000099", linestyle="--", linewidth=10,
         title="Title", width=900, x_label="xxx", y_label="yyy"
        )
        self.assertEqual(chart.series().name(), "squares")
        self.assertEqual(chart.series().color(), "#000099")
        self.assertEqual(chart.series().linestyle(), "--")
        self.assertEqual(chart.series().linewidth(), 10)
        self.assertEqual(chart.title(), "Title")
        self.assertEqual(chart.width(), 900)
        self.assertEqual(chart.x_label(), "xxx")
        self.assertEqual(chart.y_label(), "yyy")



class ScatterChartCreationTests(TestCase):

    def test_can_create_scatter_chart(self):
        chart = scatter((1, 1), (2, 4), (3, 9))
        self.assertIsInstance(chart, AxisChart)


    def test_default_scatter_color_is_first_omnicanvas_color(self):
        chart = scatter((1, 1), (2, 4), (3, 9))
        self.assertEqual(chart.series().color(), colors[0])


    def test_can_create_scatter_chart_with_line_properties(self):
        chart = scatter(
         (1, 1), (2, 4), (3, 9),
         name="squares", color="#000099", size=7, linewidth=10,
        )
        self.assertEqual(chart.series().name(), "squares")
        self.assertEqual(chart.series().color(), "#000099")
        self.assertEqual(chart.series().size(), 7)
        self.assertEqual(chart.series().linewidth(), 10)


    def test_can_create_scatter_chart_with_chart_properties(self):
        chart = scatter(
         (1, 1), (2, 4), (3, 9),
         name="squares", color="#000099", size=7, linewidth=10,
         title="Title", width=900, x_label="xxx", y_label="yyy"
        )
        self.assertEqual(chart.series().name(), "squares")
        self.assertEqual(chart.series().color(), "#000099")
        self.assertEqual(chart.series().size(), 7)
        self.assertEqual(chart.series().linewidth(), 10)
        self.assertEqual(chart.title(), "Title")
        self.assertEqual(chart.width(), 900)
        self.assertEqual(chart.x_label(), "xxx")
        self.assertEqual(chart.y_label(), "yyy")
