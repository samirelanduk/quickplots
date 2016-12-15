class Series:

    def __init__(self, *data):
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
