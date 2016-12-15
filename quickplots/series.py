class Series:

    def __init__(self, *data):
        self._data = []
        if len(data) == 0:
            raise ValueError("Cannot create Series with no data")
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
