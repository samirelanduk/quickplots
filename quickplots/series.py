class Series:

    def __init__(self, *data):
        if len(data) > 2 or len(data[0]) == 2:
            self._data = list(data)
        else:
            self._data = list(zip(data[0], data[1]))
