import re

class Timestamp(object):
    def __init__(self, month, year):
        super().__init__()
        if month <= 0  or month >= 13:
            raise ValueError("Month {} is invalid".format(month))
        self.month = month
        self.year = year
    def __lt__(self, other):
        return self.year < other.year or self.year == other.year and self.month < other.month
    def __eq__(self, other):
        if isinstance(other, Timestamp):
            return self.year == other.year and self.month == other.month
        return False
    def __le__(self, other):
        return self < other or self == other
    def parse(timestamp):
        match = re.match("([0-9]?[0-9])/([0-9][0-9][0-9][0-9])", timestamp)
        if match != None:
            return Timestamp(int(match.group(1)), int(match.group(2)))
        raise ValueError("Format string {} is not a valid timestamp".format(timestamp))
    def __str__(self):
        return ("{}/{}".format(self.month, self.year))
    def range(start, end):
        while start <= end:
            yield start
            start = Timestamp.next(start)
    def next(t):
        if t == None:
            return None
        return Timestamp((t.month % 12) + 1, t.year + (t.month // 12))
