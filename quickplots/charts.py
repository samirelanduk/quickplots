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


    def remove_series(self, series):
        if len(self.all_series()) == 1:
            raise ValueError("Cannot remove last series from %s" % str(self))
        self._all_series.remove(series)


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


    def x_lower_limit(self, lower=None):
        if lower is None:
            return 0 if self._x_lower_limit is None else self._x_lower_limit
        else:
            if not isinstance(lower, int) and not isinstance(lower, float):
                raise TypeError(
                 "lower x limit must be numeric, not '%s'" % str(lower)
                )
            self._x_lower_limit = lower


    def x_upper_limit(self, upper=None):
        if upper is None:
            largest_x = max(
             [series.data()[-1][0] for series in self.all_series()]
            ) if self._x_upper_limit is None else self._x_upper_limit
            return largest_x
        else:
            if not isinstance(upper, int) and not isinstance(upper, float):
                raise TypeError(
                 "upper x limit must be numeric, not '%s'" % str(upper)
                )
            self._x_upper_limit = upper


    def x_limit(self, lower=None, upper=None):
        if lower is None and upper is None:
            return (self.x_lower_limit(), self.x_upper_limit())
        elif lower is not None and upper is not None:
            self.x_lower_limit(lower)
            self.x_upper_limit(upper)
        else:
            raise TypeError("Need both a lower and upper x_limit")


    def y_lower_limit(self, lower=None):
        if lower is None:
            return 0 if self._y_lower_limit is None else self._y_lower_limit
        else:
            if not isinstance(lower, int) and not isinstance(lower, float):
                raise TypeError(
                 "lower y limit must be numeric, not '%s'" % str(lower)
                )
            self._y_lower_limit = lower


    def y_upper_limit(self, upper=None):
        if upper is None:
            largest_y = max(
             [series.data()[-1][1] for series in self.all_series()]
            ) if self._y_upper_limit is None else self._y_upper_limit
            return largest_y
        else:
            if not isinstance(upper, int) and not isinstance(upper, float):
                raise TypeError(
                 "upper y limit must be numeric, not '%s'" % str(upper)
                )
            self._y_upper_limit = upper


    def y_limit(self, lower=None, upper=None):
        if lower is None and upper is None:
            return (self.y_lower_limit(), self.y_upper_limit())
        elif lower is not None and upper is not None:
            self.y_lower_limit(lower)
            self.y_upper_limit(upper)
        else:
            raise TypeError("Need both a lower and upper y_limit")


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
