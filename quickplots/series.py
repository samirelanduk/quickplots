class Series:

    def __init__(self, *data, name=None):
        self._data = []
        if len(data) == 0:
            raise ValueError("Cannot create Series with no data")

        if len(data) == 2:
            if len(data[0]) != len(data[1]):
                raise ValueError(
                 "x and y data sequences are of unequal lenth (%i and %i)" % (
                  len(data[0]), len(data[1])
                 )
                )
            for series in data:
                if not isinstance(series, list) and not isinstance(series, tuple):
                    raise TypeError(
                     "Data must be give as lists or tuples, not '%s'" % str(series)
                    )
            if len(data[0]) != 2:
                data = list(zip(data[0], data[1]))

        for point in data:
            if not isinstance(point, list) and not isinstance(point, tuple):
                raise TypeError(
                 "Data must be give as lists or tuples, not '%s'" % str(point)
                )
            for value in point:
                if not isinstance(value, int) and not isinstance(value, float):
                    raise TypeError(
                     "Data point %s contains non-numeric data" % str(point)
                    )
            if len(point) != 2:
                raise ValueError(
                 "Data points must be of length 2, which %s is not" % str(point)
                )
            self._data.append(tuple(point))
        self._data = sorted(self._data, key=lambda k: k[0])

        if not isinstance(name, str) and name is not None:
            raise TypeError("name must be str, not '%s'" % str(name))
        self._name = name
        self._chart = None


    def __repr__(self):
        return "<Series %s(%i data points)>" % (
         "'%s' " % self._name if self._name is not None else "", len(self._data)
        )


    def data(self):
        return list(self._data)


    def name(self, name=None):
        if name is None:
            return self._name
        else:
            if not isinstance(name, str) and name is not None:
                raise TypeError("name must be str, not '%s'" % str(name))
            self._name = name


    def chart(self):
        return self._chart


    def smallest_x(self):
        return self.data()[0][0]


    def largest_x(self):
        return self.data()[-1][0]


    def smallest_y(self):
        return min([datum[-1] for datum in self.data()])


    def largest_y(self):
        return max([datum[-1] for datum in self.data()])


    def add_data_point(self, x, y):
        if not isinstance(x, float) and not isinstance(x, int):
            raise TypeError("x value must be numeric, not '%s'" % str(x))
        if not isinstance(y, float) and not isinstance(y, int):
            raise TypeError("y value must be numeric, not '%s'" % str(y))
        current_last_x = self._data[-1][0]
        self._data.append((x, y))
        if x < current_last_x:
            self._data = sorted(self._data, key=lambda k: k[0])


    def remove_data_point(self, x, y):
        if len(self._data) == 1:
            raise ValueError("You cannot remove a Series' last data point")
        self._data.remove((x, y))


    def canvas_points(self):
        if self.chart():
            x_axis_min = self.chart().x_lower_limit()
            y_axis_min = self.chart().y_lower_limit()
            x_axis_max = self.chart().x_upper_limit()
            y_axis_max = self.chart().y_upper_limit()
            chart_width = self.chart().width()
            chart_height = self.chart().height()
            horizontal_padding = self.chart().horizontal_padding()
            vertical_padding = self.chart().vertical_padding()
            horizontal_margin_pixels = horizontal_padding * chart_width
            vertical_margin_pixels = vertical_padding * chart_height
            x_axis_pixels = chart_width - (2 * horizontal_margin_pixels)
            y_axis_pixels = chart_height - (2 * vertical_margin_pixels)
            x_axis_span = x_axis_max - x_axis_min
            y_axis_span = y_axis_max - y_axis_min
            x_pixels_per_point = x_axis_pixels / x_axis_span
            y_pixels_per_point = y_axis_pixels / y_axis_span
            data = []
            for x, y in self.data():
                relative_x, relative_y = x - x_axis_min, y - y_axis_min
                data.append((
                 (relative_x * x_pixels_per_point) + horizontal_margin_pixels,
                 chart_height - ((relative_y * y_pixels_per_point) + vertical_margin_pixels)
                ))
            return tuple(data)



class LineSeries(Series):

    def __init__(self, *args, color="#000000", linestyle="-", **kwargs):
        Series.__init__(self, *args, **kwargs)

        if not isinstance(color, str):
            raise TypeError("color must be str, not '%s'" % str(color))
        self._color = color
        if not isinstance(linestyle, str):
            raise TypeError("linestyle must be str, not '%s'" % str(linestyle))
        self._linestyle = linestyle


    def color(self, color=None):
        if color is None:
            return self._color
        else:
            if not isinstance(color, str):
                raise TypeError("color must be str, not '%s'" % str(color))
            self._color = color
