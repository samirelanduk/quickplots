from unittest import TestCase
from unittest.mock import patch, Mock
from omnicanvas import Canvas, colors
from omnicanvas.graphics import Text, Rectangle, Polyline
from quickplots.charts import AxisChart, Chart, determine_ticks
from quickplots.series import Series, LineSeries, ScatterSeries

class AxisChartTest(TestCase):

    def setUp(self):
        self.series1 = LineSeries((1, 1), (2, 4), (3, 9), name="series1")
        self.series2 = LineSeries((10, 20), (100, 200), (1000, 2000), name="series2")
        self.series3 = LineSeries((-10, -5), (23, 45), (-1, 2), name="series3")


class AxisChartCreationTests(AxisChartTest):

    def test_can_create_axis_chart(self):
        chart = AxisChart(self.series1)
        self.assertIsInstance(chart, Chart)
        self.assertEqual(chart._all_series, [self.series1])
        self.assertEqual(chart._x_label, "")
        self.assertEqual(chart._y_label, "")
        self.assertEqual(chart._horizontal_padding, 0.1)
        self.assertEqual(chart._vertical_padding, 0.1)
        self.assertEqual(chart._x_lower_limit, None)
        self.assertEqual(chart._x_upper_limit, None)
        self.assertEqual(chart._y_lower_limit, None)
        self.assertEqual(chart._y_upper_limit, None)


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


    def test_series_know_about_chart(self):
        chart = AxisChart(self.series1, self.series2, self.series3)
        self.assertIs(self.series1.chart(), chart)
        self.assertIs(self.series2.chart(), chart)
        self.assertIs(self.series3.chart(), chart)


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



class AxisChartBasicPropertyTests(AxisChartTest):

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


    def test_series_refers_to_first_series(self):
        chart = AxisChart(self.series1)
        self.assertIs(chart.series(), self.series1)
        chart = AxisChart(self.series1, self.series2, self.series3)
        self.assertIs(chart.series(), self.series1)



class AxisChartAxisLabelTests(AxisChartTest):

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



class AxisChartPaddingTests(AxisChartTest):

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



class AxisChartValueExtremesTests(AxisChartTest):

    def test_chart_knows_its_smallest_values(self):
        chart = AxisChart(self.series1)
        self.assertEqual(chart.smallest_x(), 1)
        self.assertEqual(chart.smallest_y(), 1)
        chart = AxisChart(self.series2)
        self.assertEqual(chart.smallest_x(), 10)
        self.assertEqual(chart.smallest_y(), 20)
        chart = AxisChart(self.series3)
        self.assertEqual(chart.smallest_x(), -10)
        self.assertEqual(chart.smallest_y(), -5)
        chart = AxisChart(self.series1, self.series2, self.series3)
        self.assertEqual(chart.smallest_x(), -10)
        self.assertEqual(chart.smallest_y(), -5)


    def test_chart_knows_its_largest_values(self):
        chart = AxisChart(self.series1)
        self.assertEqual(chart.largest_x(), 3)
        self.assertEqual(chart.largest_y(), 9)
        chart = AxisChart(self.series2)
        self.assertEqual(chart.largest_x(), 1000)
        self.assertEqual(chart.largest_y(), 2000)
        chart = AxisChart(self.series3)
        self.assertEqual(chart.largest_x(), 23)
        self.assertEqual(chart.largest_y(), 45)
        chart = AxisChart(self.series1, self.series2, self.series3)
        self.assertEqual(chart.largest_x(), 1000)
        self.assertEqual(chart.largest_y(), 2000)



class AxisChartAxisLimitTests(AxisChartTest):

    def test_lower_x_limit_defaults_to_zero(self):
        chart = AxisChart(self.series1)
        self.assertEqual(chart.x_lower_limit(), 0)


    def test_lower_x_limit_does_not_default_to_zero_when_negative(self):
        chart = AxisChart(self.series3)
        self.assertEqual(chart.x_lower_limit(), -10)


    def test_lower_x_limit_is_zero_when_only_one_x_value(self):
        series = Series((1, 2), (1, 3), (1, 4))
        chart = AxisChart(series)
        self.assertEqual(chart.x_lower_limit(), 0)


    def test_lower_x_limit_adjusts_when_only_one_negative_x_value(self):
        series = Series((-1, 2), (-1, 3), (-1, 4))
        chart = AxisChart(series)
        self.assertEqual(chart.x_lower_limit(), -2)
        series = Series((-1.5, 2), (-1.5, 3), (-1.5, 4))
        chart = AxisChart(series)
        self.assertEqual(chart.x_lower_limit(), -2)


    def test_can_manually_set_lower_x_limit(self):
        chart = AxisChart(self.series1)
        chart.x_lower_limit(2)
        self.assertEqual(chart.x_lower_limit(), 2)
        chart.x_lower_limit(-200)
        self.assertEqual(chart.x_lower_limit(), -200)


    def test_manually_set_lower_x_limit_must_be_numeric(self):
        chart = AxisChart(self.series1)
        with self.assertRaises(TypeError):
            chart.x_lower_limit("2")
        chart.x_lower_limit(2.5)


    def test_manually_set_lower_x_limit_cannot_be_greater_than_upper_limit(self):
        chart = AxisChart(self.series1)
        with self.assertRaises(ValueError):
            chart.x_lower_limit(3)
        with self.assertRaises(ValueError):
            chart.x_lower_limit(3.5)
        with self.assertRaises(ValueError):
            chart.x_lower_limit(4)


    def test_lower_y_limit_defaults_to_zero(self):
        chart = AxisChart(self.series1)
        self.assertEqual(chart.y_lower_limit(), 0)


    def test_lower_y_limit_does_not_default_to_zero_when_negative(self):
        chart = AxisChart(self.series3)
        self.assertEqual(chart.y_lower_limit(), -5)


    def test_lower_y_limit_is_zero_when_only_one_y_value(self):
        series = Series((1, 1), (2, 1), (3, 1))
        chart = AxisChart(series)
        self.assertEqual(chart.y_lower_limit(), 0)


    def test_lower_y_limit_adjusts_when_only_one_negative_y_value(self):
        series = Series((1, -4), (2, -4), (3, -4))
        chart = AxisChart(series)
        self.assertEqual(chart.y_lower_limit(), -5)
        series = Series((1, -4.5), (2, -4.5), (3, -4.5))
        chart = AxisChart(series)
        self.assertEqual(chart.y_lower_limit(), -5)


    def test_can_manually_set_lower_y_limit(self):
        chart = AxisChart(self.series1)
        chart.y_lower_limit(2)
        self.assertEqual(chart.y_lower_limit(), 2)
        chart.y_lower_limit(-200)
        self.assertEqual(chart.y_lower_limit(), -200)


    def test_manually_set_lower_y_limit_must_be_numeric(self):
        chart = AxisChart(self.series1)
        with self.assertRaises(TypeError):
            chart.y_lower_limit("2")
        chart.y_lower_limit(2.5)


    def test_manually_set_lower_y_limit_cannot_be_greater_than_upper_limit(self):
        chart = AxisChart(self.series1)
        with self.assertRaises(ValueError):
            chart.y_lower_limit(9)
        with self.assertRaises(ValueError):
            chart.y_lower_limit(9.5)
        with self.assertRaises(ValueError):
            chart.y_lower_limit(10)


    def test_upper_x_limit_defaults_to_largest_x(self):
        chart = AxisChart(self.series1)
        self.assertEqual(chart.x_upper_limit(), 3)
        chart = AxisChart(self.series2)
        self.assertEqual(chart.x_upper_limit(), 1000)
        chart = AxisChart(self.series3)
        self.assertEqual(chart.x_upper_limit(), 23)


    def test_upper_x_limit_adjusts_when_only_one_x_value(self):
        series = Series((1, 2), (1, 3), (1, 4))
        chart = AxisChart(series)
        self.assertEqual(chart.x_upper_limit(), 2)
        series = Series((1.5, 2), (1.5, 3), (1.5, 4))
        chart = AxisChart(series)
        self.assertEqual(chart.x_upper_limit(), 2)
        series = Series((-1, 2), (-1, 3), (-1, 4))
        chart = AxisChart(series)
        self.assertEqual(chart.x_upper_limit(), 0)
        series = Series((-1.5, 2), (-1.5, 3), (-1.5, 4))
        chart = AxisChart(series)
        self.assertEqual(chart.x_upper_limit(), -1)


    def test_can_manually_set_upper_x_limit(self):
        chart = AxisChart(self.series1)
        chart.x_upper_limit(2)
        self.assertEqual(chart.x_upper_limit(), 2)
        chart.x_upper_limit(200)
        self.assertEqual(chart.x_upper_limit(), 200)


    def test_manually_set_upper_x_limit_must_be_numeric(self):
        chart = AxisChart(self.series1)
        with self.assertRaises(TypeError):
            chart.x_upper_limit("2")
        chart.x_upper_limit(2.5)


    def test_manually_set_lower_x_limit_cannot_be_less_than_lower_limit(self):
        chart = AxisChart(self.series1)
        with self.assertRaises(ValueError):
            chart.x_upper_limit(1)
        with self.assertRaises(ValueError):
            chart.x_upper_limit(0.5)
        with self.assertRaises(ValueError):
            chart.x_upper_limit(0)


    def test_upper_y_limit_defaults_to_largest_y(self):
        chart = AxisChart(self.series1)
        self.assertEqual(chart.y_upper_limit(), 9)
        chart = AxisChart(self.series2)
        self.assertEqual(chart.y_upper_limit(), 2000)
        chart = AxisChart(self.series3)
        self.assertEqual(chart.y_upper_limit(), 45)


    def test_upper_y_limit_adjusts_when_only_one_y_value(self):
        series = Series((1, 2), (2, 2), (3, 2))
        chart = AxisChart(series)
        self.assertEqual(chart.y_upper_limit(), 3)
        series = Series((1, 2.5), (2, 2.5), (3, 2.5))
        chart = AxisChart(series)
        self.assertEqual(chart.y_upper_limit(), 3)
        series = Series((1, -2), (2, -2), (3, -2))
        chart = AxisChart(series)
        self.assertEqual(chart.y_upper_limit(), -1)
        series = Series((1, -2.5), (2, -2.5), (3, -2.5))
        chart = AxisChart(series)
        self.assertEqual(chart.y_upper_limit(), -2)


    def test_can_manually_set_upper_y_limit(self):
        chart = AxisChart(self.series1)
        chart.y_upper_limit(2)
        self.assertEqual(chart.y_upper_limit(), 2)
        chart.y_upper_limit(200)
        self.assertEqual(chart.y_upper_limit(), 200)


    def test_manually_set_upper_y_limit_must_be_numeric(self):
        chart = AxisChart(self.series1)
        with self.assertRaises(TypeError):
            chart.y_upper_limit("2")
        chart.y_upper_limit(2.5)


    def test_manually_set_lower_y_limit_cannot_be_less_than_lower_limit(self):
        chart = AxisChart(self.series1)
        with self.assertRaises(ValueError):
            chart.y_upper_limit(1)
        with self.assertRaises(ValueError):
            chart.y_upper_limit(0.5)
        with self.assertRaises(ValueError):
            chart.y_upper_limit(0)



class AxisChartTickTests(AxisChartTest):

    def test_ticks_are_tuple(self):
        chart = AxisChart(self.series1)
        self.assertIsInstance(chart.x_ticks(), tuple)
        self.assertIsInstance(chart.y_ticks(), tuple)


    def test_tick_determiner_produces_correct_values_when_zero_based(self):
        self.assertEqual(
         determine_ticks(0, 10),
         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        )
        self.assertEqual(
         determine_ticks(0, 12.4),
         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        )
        self.assertEqual(
         determine_ticks(0, 12.5),
         [0, 10]
        )
        self.assertEqual(
         determine_ticks(0, 75),
         [0, 10, 20, 30, 40, 50, 60, 70]
        )
        self.assertEqual(
         determine_ticks(0, 100),
         [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        )
        self.assertEqual(
         determine_ticks(0, 124),
         [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
        )
        self.assertEqual(
         determine_ticks(0, 125),
         [0, 100]
        )
        self.assertEqual(
         determine_ticks(0, 54321),
         [0, 10000, 20000, 30000, 40000, 50000]
        )


    def test_tick_determiner_produces_correct_values_when_not_zero_based(self):
        self.assertEqual(
         determine_ticks(7, 12),
         [7, 8, 9, 10, 11, 12]
        )
        self.assertEqual(
         determine_ticks(11, 1009),
         [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
        )
        self.assertEqual(
         determine_ticks(-500, 500),
         [-500, -400, -300, -200, -100, 0, 100, 200, 300, 400, 500]
        )
        self.assertEqual(
         determine_ticks(-500, 749),
         [-500, -400, -300, -200, -100, 0, 100, 200, 300, 400, 500, 600, 700]
        )
        self.assertEqual(
         determine_ticks(-500, 750),
         [0]
        )


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


    def test_adding_series_updates_its_chart(self):
        chart = AxisChart(self.series1)
        chart.add_series(self.series2)
        self.assertIs(self.series2.chart(), chart)


    def test_can_remove_series(self):
        chart = AxisChart(self.series1, self.series2)
        chart.remove_series(self.series1)
        self.assertEqual(chart.all_series(), [self.series2])


    def test_cannot_remove_last_series(self):
        chart = AxisChart(self.series1)
        with self.assertRaises(ValueError):
            chart.remove_series(self.series1)


    def test_removing_series_breaks_its_connection(self):
        chart = AxisChart(self.series1, self.series2)
        chart.remove_series(self.series1)
        self.assertIs(self.series2.chart(), chart)
        self.assertIs(self.series1.chart(), None)


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



class AxisChartColorSelectionTests(AxisChartTest):

    def test_chart_picks_first_omnicanvas_color_if_no_omnicanvas_colors(self):
        chart = AxisChart(self.series1)
        self.assertEqual(chart.next_color(), colors[0])


    def test_chart_works_through_omnicanvas_colors(self):
        chart = AxisChart(self.series1)
        self.series1.color(colors[0])
        self.assertEqual(chart.next_color(), colors[1])
        chart = AxisChart(self.series1, self.series2)
        self.series2.color(colors[1])
        self.assertEqual(chart.next_color(), colors[2])


    def test_chart_returns_random_colors_when_all_used(self):
        from omnicanvas.color import is_valid_color
        series = [Series((1, 1), (2, 2), color=color) for color in colors]
        chart = AxisChart(*series)
        self.assertTrue(is_valid_color(chart.next_color()))


    def test_chart_can_identify_unused_colors_before_using_randoms(self):
        series = [Series((1, 1), (2, 2), color=color) for color in colors]
        series.pop(4)
        chart = AxisChart(*series)
        self.assertEqual(chart.next_color(), colors[4])



class AxisChartQuickAddTests(AxisChartTest):

    def test_can_quick_add_line_series(self):
        chart = AxisChart(self.series1)
        chart.line((1, 1), (2, 8), (3, 27))
        self.assertEqual(len(chart.all_series()), 2)
        self.assertIsInstance(chart.all_series()[-1], LineSeries)
        self.assertEqual(
         chart.all_series()[-1].data(),
         [(1, 1), (2, 8), (3, 27)]
        )


    def test_added_line_uses_next_color(self):
        chart = AxisChart(self.series1)
        next_color = chart.next_color()
        chart.line((1, 1), (2, 8), (3, 27))
        self.assertEqual(chart.all_series()[-1].color(), next_color)
        next_color = chart.next_color()
        chart.line((1, 1), (2, 8), (3, 27))
        self.assertEqual(chart.all_series()[-1].color(), next_color)


    def test_can_quick_add_line_series_with_series_keyword_arguments(self):
        chart = AxisChart(self.series1)
        chart.line(
         (1, 1), (2, 8), (3, 27),
         name="cubes", color="#ADADAD", linestyle="..", linewidth=10
        )
        self.assertEqual(chart.all_series()[-1].name(), "cubes")
        self.assertEqual(chart.all_series()[-1].color(), "#ADADAD")
        self.assertEqual(chart.all_series()[-1].linestyle(), "..")
        self.assertEqual(chart.all_series()[-1].linewidth(), 10)


    def test_can_quick_add_scatter_series(self):
        chart = AxisChart(self.series1)
        chart.scatter((1, 1), (2, 8), (3, 27))
        self.assertEqual(len(chart.all_series()), 2)
        self.assertIsInstance(chart.all_series()[-1], ScatterSeries)
        self.assertEqual(
         chart.all_series()[-1].data(),
         [(1, 1), (2, 8), (3, 27)]
        )


    def test_added_scatter_uses_next_color(self):
        chart = AxisChart(self.series1)
        next_color = chart.next_color()
        chart.scatter((1, 1), (2, 8), (3, 27))
        self.assertEqual(chart.all_series()[-1].color(), next_color)
        next_color = chart.next_color()
        chart.scatter((1, 1), (2, 8), (3, 27))
        self.assertEqual(chart.all_series()[-1].color(), next_color)


    def test_can_quick_add_scatter_series_with_series_keyword_arguments(self):
        chart = AxisChart(self.series1)
        chart.scatter(
         (1, 1), (2, 8), (3, 27),
         name="cubes", color="#ADADAD", size=0.5, linewidth=10
        )
        self.assertEqual(chart.all_series()[-1].name(), "cubes")
        self.assertEqual(chart.all_series()[-1].color(), "#ADADAD")
        self.assertEqual(chart.all_series()[-1].size(), 0.5)
        self.assertEqual(chart.all_series()[-1].linewidth(), 10)



class AxisChartCanvasTests(AxisChartTest):

    def setUp(self):
        AxisChartTest.setUp(self)
        self.chart = AxisChart(self.series1, title="Test AxisChart")


    def test_can_create_basic_canvas(self):
        canvas = self.chart.create()
        title = canvas.get_graphic_by_name("title")
        self.assertEqual(title.text(), "Test AxisChart")


    def test_title_centered_in_space_between_axis_top_and_canvas_top(self):
        canvas = self.chart.create()
        title = canvas.get_graphic_by_name("title")
        self.assertEqual(title.y(), 25)
        self.assertEqual(title.vertical_align(), "center")


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


    @patch("quickplots.series.LineSeries.write_to_canvas")
    def test_series_canvas_writer_is_called(self, mock):
        canvas = self.chart.create()
        self.assertTrue(mock.called)


    def test_series_paint_themselves_to_canvas(self):
        canvas = self.chart.create()
        line = canvas.get_graphic_by_name("series1")
        self.assertIsInstance(line, Polyline)


    def test_multiple_series_can_be_written_to_canvas(self):
        self.chart = AxisChart(
         self.series1, self.series2, self.series3, title="Test AxisChart"
        )
        canvas = self.chart.create()
        line1 = canvas.get_graphic_by_name("series1")
        line2 = canvas.get_graphic_by_name("series2")
        line3 = canvas.get_graphic_by_name("series3")
        self.assertIsInstance(line1, Polyline)
        self.assertIsInstance(line2, Polyline)
        self.assertIsInstance(line3, Polyline)


    def test_series_are_before_everything_else(self):
        canvas = self.chart.create()
        line = canvas.get_graphic_by_name("series1")
        self.assertIs(line, canvas.graphics()[0])


    def test_white_rectangles_block_out_area_beyond_axes(self):
        canvas = self.chart.create()
        block1 = canvas.get_graphic_by_name("block-w")
        block2 = canvas.get_graphic_by_name("block-n")
        block3 = canvas.get_graphic_by_name("block-s")
        block4 = canvas.get_graphic_by_name("block-e")
        axes = canvas.get_graphic_by_name("axes")
        for block in block1, block2, block3, block4:
            self.assertIsInstance(block, Rectangle)
            self.assertEqual(block.fill_color(), "#FFFFFF")
            self.assertEqual(block.opacity(), 1)
            self.assertEqual(block.line_width(), 0)
        self.assertEqual(block1.x(), 0)
        self.assertEqual(block1.y(), 0)
        self.assertEqual(block1.width(), axes.x())
        self.assertEqual(block1.height(), canvas.height())
        self.assertEqual(block2.x(), 0)
        self.assertEqual(block2.y(), 0)
        self.assertEqual(block2.width(), canvas.width())
        self.assertEqual(block2.height(), axes.y())
        self.assertEqual(block3.x(), 0)
        self.assertEqual(block3.y(), axes.y() + axes.height())
        self.assertEqual(block3.width(), canvas.width())
        self.assertEqual(block3.height(), canvas.height() - (axes.y() + axes.height()))
        self.assertEqual(block4.x(), axes.x() + axes.width())
        self.assertEqual(block4.y(), 0)
        self.assertEqual(block4.width(), canvas.width() - (axes.x() + axes.width()))
        self.assertEqual(block4.height(), canvas.height())


    def test_white_blockers_are_immediately_after_series(self):
        canvas = self.chart.create()
        line = canvas.get_graphic_by_name("series1")
        block1 = canvas.get_graphic_by_name("block-w")
        block2 = canvas.get_graphic_by_name("block-n")
        block3 = canvas.get_graphic_by_name("block-e")
        block4 = canvas.get_graphic_by_name("block-s")
        start_index = canvas.graphics().index(line)
        self.assertEqual(canvas.graphics().index(block1), start_index + 1)
        self.assertEqual(canvas.graphics().index(block2), start_index + 2)
        self.assertEqual(canvas.graphics().index(block3), start_index + 3)
        self.assertEqual(canvas.graphics().index(block4), start_index + 4)
