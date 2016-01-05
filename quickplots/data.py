import datetime
import collections

class DatetimeDatum:
    """A datetime in the streets, a number in the sheets"""

    def __init__(self, dt):
        self.dt = dt
        if isinstance(self.dt, datetime.datetime):
            self.value = dt.timestamp()
        else:
            self.value = datetime.datetime(year=dt.year, month=dt.month, day=dt.day).timestamp()


    def __repr__(self):
        if isinstance(self.dt, datetime.datetime):
            return str(self.dt)
        else:
            return self.dt.strftime("%Y-%b-%d")


    def __add__(self, other):
        return self.value + other


    def __radd__(self, other):
        return self.value + other


    def __sub__(self, other):
        return self.value - other


    def __rsub__(self, other):
        return other - self.value


    def __lt__(self, other):
        return self.value < other


    def __le__(self, other):
        return self.value <= other


    def __gt__(self, other):
        return self.value > other


    def __ge__(self, other):
        return self.value >= other


    def __eq__(self, other):
        return self.value == other


    def __ne__(self, other):
        return self.value != other



class DataSequence(list):
    """A mutable sequence which might contain date data."""

    def __init__(self, sequence):
        list.__init__(self, check_series_for_dates(sequence))

    def __setitem__(self, key, item):
        list.__setitem__(self, key, check_value_for_date(item))

    def append(self, item):
        list.append(self, check_value_for_date(item))



class Tick:

    def __init__(self, value, label=None):
        self.value = check_value_for_date(value)
        self.label = str(self.value) if label is None else label


    def __repr__(self):
        return "%s (%s)" % (str(self.value), self.label)


class TickSequence(list):

    def __setitem__(self, key, value):
        if isinstance(value, collections.Sequence) and not isinstance(value, str):
            list.__setitem__(self, key, Tick(value[0], value[1]))
        else:
            list.__setitem__(self, key, Tick(value))


    def append(self, value):
        if isinstance(value, collections.Sequence) and not isinstance(value, str):
            list.append(self, Tick(value[0], value[1]))
        else:
            list.append(self, Tick(value))



class Series(list):
    """A sequence of length-2 DataSequences"""

    def __init__(self, series):
        series = [DataSequence(d) for d in series]
        for datum in series:
            assert len(datum) == 2
        list.__init__(self, series)


    def __setitem__(self, key, datum):
        assert len(datum) == 2
        list.__setitem__(self, key, check_series_for_dates(datum))


    def append(self, datum):
        assert len(datum) == 2
        list.append(self, check_series_for_dates(item))



def check_value_for_date(value):
    if isinstance(value, datetime.date):
        if isinstance(value, datetime.datetime):
            return DatetimeDatum(value)
        else:
            return DatetimeDatum(datetime.date(value.year, value.month, value.day))
    else:
        return value


def check_series_for_dates(series):
    filtered = [check_value_for_date(v) for v in series]
    return type(series)(filtered)
