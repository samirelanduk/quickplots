import math
from omnicanvas import Canvas
from .series import Series

class Chart:

    def __init__(self, title="", width=700, height=500):
        if not isinstance(title, str):
            raise TypeError("title must be str, not '%s'" % str(title))
        self._title = title

        if not isinstance(width, int) and not isinstance(width, float):
            raise TypeError("width must be numeric, not '%s'" % str(width))
        self._width = width

        if not isinstance(height, int) and not isinstance(height, float):
            raise TypeError("height must be numeric, not '%s'" % str(height))
        self._height = height


    def __repr__(self):
        return "<Chart (%i×%i)>" % (self._width, self._height)


    def title(self, title=None):
        if title is None:
            return self._title
        else:
            if not isinstance(title, str):
                raise TypeError("title must be str, not '%s'" % str(title))
            self._title = title


    def width(self, width=None):
        if width is None:
            return self._width
        else:
            if not isinstance(width, int) and not isinstance(width, float):
                raise TypeError("width must be numeric, not '%s'" % str(width))
            self._width = width


    def height(self, height=None):
        if height is None:
            return self._height
        else:
            if not isinstance(height, int) and not isinstance(height, float):
                raise TypeError("height must be numeric, not '%s'" % str(height))
            self._height = height


    def create(self):
        canvas = Canvas(self.width(), self.height())
        canvas.add_text(
         self.width() / 2, 0, self.title(),
         vertical_align="bottom", name="title"
        )
        return canvas


class AxisChart(Chart):

    def __init__(self, *series, x_label="", y_label="", **kwargs):
        Chart.__init__(self, **kwargs)

        for s in series:
            if not isinstance(s, Series):
                raise TypeError("'%s' is not a Series" % str(s))
        if len(series) == 0:
            raise ValueError("AxisChart needs at least one series")
        self._all_series = list(series)
        for s in series:
            s._chart = self

        if not isinstance(x_label, str):
            raise TypeError("x_label must be str, not '%s'" % str(x_label))
        self._x_label = x_label
        if not isinstance(y_label, str):
            raise TypeError("y_label must be str, not '%s'" % str(y_label))
        self._y_label = y_label

        self._horizontal_padding = 0.1
        self._vertical_padding = 0.1
        self._x_lower_limit = None
        self._x_upper_limit = None
        self._y_lower_limit = None
        self._y_upper_limit = None


    def __repr__(self):
        return "<AxisChart (%i series)>" % len(self._all_series)


    def all_series(self):
        return list(self._all_series)


    def series(self):
        return self._all_series[0]


    def add_series(self, series):
        if not isinstance(series, Series):
            raise TypeError("'%s' is not a Series" % str(series))
        self._all_series.append(series)
        series._chart = self


    def remove_series(self, series):
        if len(self.all_series()) == 1:
            raise ValueError("Cannot remove last series from %s" % str(self))
        self._all_series.remove(series)
        series._chart = None


    def get_series_by_name(self, name):
        if not isinstance(name, str):
            raise TypeError(
             "Can only search series by str name, not '%s'" % str(name)
            )
        for series in self.all_series():
            if series.name() == name:
                return series


    def x_label(self, x_label=None):
        if x_label is None:
            return self._x_label
        else:
            if not isinstance(x_label, str):
                raise TypeError("x_label must be str, not '%s'" % str(x_label))
            self._x_label = x_label


    def y_label(self, y_label=None):
        if y_label is None:
            return self._y_label
        else:
            if not isinstance(y_label, str):
                raise TypeError("y_label must be str, not '%s'" % str(y_label))
            self._y_label = y_label


    def horizontal_padding(self, padding=None):
        if padding is None:
            return self._horizontal_padding
        else:
            if not isinstance(padding, float):
                raise TypeError("padding must be float, not '%s'" % str(padding))
            if not 0 < padding < 0.5:
                raise ValueError(
                 "padding must be between 0 and 0.5 (not inclusive), not '%s'" % str(padding)
                )
            self._horizontal_padding = padding


    def vertical_padding(self, padding=None):
        if padding is None:
            return self._vertical_padding
        else:
            if not isinstance(padding, float):
                raise TypeError("padding must be float, not '%s'" % str(padding))
            if not 0 < padding < 0.5:
                raise ValueError(
                 "padding must be between 0 and 0.5 (not inclusive), not '%s'" % str(padding)
                )
            self._vertical_padding = padding


    def smallest_x(self):
        return min(
         [series.data()[0][0] for series in self.all_series()]
        )


    def largest_x(self):
        return max(
         [series.data()[-1][0] for series in self.all_series()]
        )


    def smallest_y(self):
        return min(
         [series.smallest_y() for series in self.all_series()]
        )


    def largest_y(self):
        return max(
         [series.largest_y() for series in self.all_series()]
        )


    def x_lower_limit(self, limit=None):
        if limit is None:
            if self._x_lower_limit is None:
                if self.smallest_x() < 0:
                    if self.smallest_x() == self.largest_x():
                        return int(self.smallest_x() - 1)
                    else:
                        return self.smallest_x()
                else:
                    return 0
            else:
                return self._x_lower_limit
        else:
            if not isinstance(limit, int) and not isinstance(limit, float):
                raise TypeError(
                 "lower x limit must be numeric, not '%s'" % str(limit)
                )
            if limit >= self.largest_x():
                raise ValueError(
                 "lower x limit must be less than upper limit (%s), not %s" % (
                  str(self.largest_x()), str(limit)
                 )
                )
            self._x_lower_limit = limit


    def y_lower_limit(self, limit=None):
        if limit is None:
            if self._y_lower_limit is None:
                if self.smallest_y() < 0:
                    if self.smallest_y() == self.largest_y():
                        return int(self.smallest_y() - 1)
                    else:
                        return self.smallest_y()
                else:
                    return 0
            else:
                return self._y_lower_limit
        else:
            if not isinstance(limit, int) and not isinstance(limit, float):
                raise TypeError(
                 "lower y limit must be numeric, not '%s'" % str(limit)
                )
            if limit >= self.largest_y():
                raise ValueError(
                 "lower y limit must be less than upper limit (%s), not %s" % (
                  str(self.largest_y()), str(limit)
                 )
                )
            self._y_lower_limit = limit


    def x_upper_limit(self, limit=None):
        if limit is None:
            if self._x_upper_limit is None:
                if self.smallest_x() == self.largest_x():
                    if int(self.largest_x()) == float(self.largest_x()):
                        return self.largest_x() + 1
                    else:
                        return math.ceil(self.largest_x())
                else:
                    return self.largest_x()
            else:
                return self._x_upper_limit
        else:
            if not isinstance(limit, int) and not isinstance(limit, float):
                raise TypeError(
                 "upper x limit must be numeric, not '%s'" % str(limit)
                )
            if limit <= self.smallest_x():
                raise ValueError(
                 "upper x limit must be greater than lower limit (%s), not %s" % (
                  str(self.smallest_x()), str(limit)
                 )
                )
            self._x_upper_limit = limit


    def y_upper_limit(self, limit=None):
        if limit is None:
            if self._y_upper_limit is None:
                if self.smallest_y() == self.largest_y():
                    if int(self.largest_y()) == float(self.largest_y()):
                        return self.largest_y() + 1
                    else:
                        return math.ceil(self.largest_y())
                else:
                    return self.largest_y()
            else:
                return self._y_upper_limit
        else:
            if not isinstance(limit, int) and not isinstance(limit, float):
                raise TypeError(
                 "upper y limit must be numeric, not '%s'" % str(limit)
                )
            if limit <= self.smallest_y():
                raise ValueError(
                 "upper y limit must be greater than lower limit (%s), not %s" % (
                  str(self.smallest_y()), str(limit)
                 )
                )
            self._y_upper_limit = limit


    def create(self):
        canvas = Chart.create(self)

        canvas.add_rectangle(
         self.horizontal_padding() * canvas.width(),
         self.vertical_padding() * canvas.height(),
         canvas.width() - (2 * self.horizontal_padding() * canvas.width()),
         canvas.height() - (2 * self.vertical_padding() * canvas.height()),
         name="axes",
         opacity=0
        )

        if self.x_label():
            canvas.add_text(
             canvas.width() / 2,
             canvas.height() - (self.vertical_padding() * canvas.height() * 0.5),
             self.x_label(),
             name="x_label"
            )
        y_label_x = self.horizontal_padding() * canvas.width() * 0.5
        if self.y_label():
            canvas.add_text(
             y_label_x,
             canvas.height() * 0.5,
             self.y_label(),
             rotation=(y_label_x, canvas.height() * 0.5, 270),
             name="y_label"
            )
        return canvas
