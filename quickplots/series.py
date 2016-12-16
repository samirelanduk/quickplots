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


    def __repr__(self):
        return "<Series (%i data points)>" % len(self._data)


    def data(self):
        return list(self._data)


    def name(self, name=None):
        if name is None:
            return self._name
        else:
            if not isinstance(name, str) and name is not None:
                raise TypeError("name must be str, not '%s'" % str(name))
            self._name = name


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
