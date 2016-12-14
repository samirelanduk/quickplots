from omnicanvas import Canvas

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
        canvas._title_graphic = canvas.graphics()[-1]
        return canvas


class AxisChart(Chart):

    def __init__(self, *args, **kwargs):
        Chart.__init__(self, *args, **kwargs)
        self._all_series = []


    def __repr__(self):
        return "<AxisChart (%i series)>" % len(self._all_series)


    def create(self):
        canvas = Chart.create(self)
        canvas.add_rectangle(0, 0, 10, 10, name="axes")
        canvas._axes_graphic = canvas.graphics()[-1]
        return canvas
