class Series:

    def __init__(self, *data):
        if len(data) == 2:
            self._data = list(zip(data[0], data[1]))
        else:
            self._data = list(data)
