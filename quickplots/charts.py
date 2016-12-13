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


    def width(self):
        return self._width


    def height(self):
        return self._height
