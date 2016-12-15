class Series:

    def __init__(self, *data):
        self._data = []
        for point in data:
            if not isinstance(point, list) and not isinstance(point, tuple):
                raise TypeError(
                 "Data must be give as lists or tuples, not '%s'" % str(point)
                )
            else:
                self._data.append(tuple(point))
