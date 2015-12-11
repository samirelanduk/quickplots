import datetime

class DatetimeDatum:
    """A datetime in the streets, a number in the sheets"""

    def __init__(self, dt):
        self.dt = datetime.date
        self.value = dt.timestamp()


    def __repr__(self):
        return str(self.dt)


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


def check_value_for_date(value):
    if isinstance(value, datetime.date):
        if isinstance(value, datetime.datetime):
            return DatetimeDatum(value)
        else:
            return DatetimeDatum(datetime.datetime(value.year, value.month, value.day))
    else:
        return value


def check_series_for_dates(series):
    filtered = [check_value_for_date(v) for v in series]
    return type(series)(filtered)
