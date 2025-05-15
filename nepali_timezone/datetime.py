"""
Nepali datetime implementation.
"""

from datetime import datetime, timedelta as dt_timedelta
import nepali_datetime
from django.utils import timezone
from .utils import get_default_timezone


class NepaliDateTime:
    """A timezone-aware Nepali datetime class using Bikram Sambat calendar."""

    def __init__(
        self, year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None
    ):
        self._nepali_dt = nepali_datetime.datetime(
            year, month, day, hour, minute, second, microsecond
        )
        self._tzinfo = tzinfo or get_default_timezone()

    @classmethod
    def from_datetime(cls, dt):
        """Convert a standard datetime to NepaliDateTime."""
        if dt.tzinfo is None:
            dt = timezone.make_aware(dt, get_default_timezone())
        nepali_dt = nepali_datetime.datetime.from_datetime(dt)
        return cls(
            year=nepali_dt.year,
            month=nepali_dt.month,
            day=nepali_dt.day,
            hour=nepali_dt.hour,
            minute=nepali_dt.minute,
            second=nepali_dt.second,
            microsecond=nepali_dt.microsecond,
            tzinfo=dt.tzinfo,
        )

    @classmethod
    def from_gregorian(
        cls, year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None
    ):
        """Create NepaliDateTime from Gregorian date."""
        gregorian_dt = datetime(year, month, day, hour, minute, second, microsecond)
        if tzinfo:
            gregorian_dt = timezone.make_aware(gregorian_dt, tzinfo)
        else:
            gregorian_dt = timezone.make_aware(gregorian_dt, get_default_timezone())
        return cls.from_datetime(gregorian_dt)

    @classmethod
    def now(cls):
        """Return current Nepali datetime."""
        return cls.from_datetime(timezone.now())

    def to_datetime(self):
        """Convert to standard Python datetime."""
        gregorian_dt = self._nepali_dt.to_datetime()
        return gregorian_dt.replace(tzinfo=self._tzinfo)

    def to_gregorian(self):
        """Convert to Gregorian datetime."""
        return self.to_datetime()

    @property
    def year(self):
        return self._nepali_dt.year

    @property
    def month(self):
        return self._nepali_dt.month

    @property
    def day(self):
        return self._nepali_dt.day

    @property
    def hour(self):
        return self._nepali_dt.hour

    @property
    def minute(self):
        return self._nepali_dt.minute

    @property
    def second(self):
        return self._nepali_dt.second

    @property
    def microsecond(self):
        return self._nepali_dt.microsecond

    @property
    def tzinfo(self):
        return self._tzinfo

    def __str__(self):
        return (
            self._nepali_dt.strftime("%Y-%m-%d %H:%M:%S")
            + f" {self._tzinfo.tzname(None)}"
        )

    def __add__(self, other):
        if isinstance(other, dt_timedelta):
            gregorian_dt = self.to_datetime() + other
            return NepaliDateTime.from_datetime(gregorian_dt)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, dt_timedelta):
            gregorian_dt = self.to_datetime() - other
            return NepaliDateTime.from_datetime(gregorian_dt)
        return NotImplemented


def is_aware(dt):
    """Check if a datetime or NepaliDateTime is timezone-aware."""
    if isinstance(dt, NepaliDateTime):
        return (
            dt.tzinfo is not None and dt.tzinfo.utcoffset(dt.to_datetime()) is not None
        )
    return timezone.is_aware(dt)


def is_naive(dt):
    """Check if a datetime or NepaliDateTime is naive."""
    return not is_aware(dt)


def make_aware(dt, tz=None):
    """Make a naive datetime or NepaliDateTime timezone-aware."""
    if is_aware(dt):
        return dt
    tzinfo = tz or get_default_timezone()
    if isinstance(dt, NepaliDateTime):
        gregorian_dt = dt.to_datetime()
        aware_dt = timezone.make_aware(gregorian_dt, tzinfo)
        return NepaliDateTime.from_datetime(aware_dt)
    return NepaliDateTime.from_datetime(timezone.make_aware(dt, tzinfo))


def make_naive(dt, tz=None):
    """Make an aware datetime or NepaliDateTime timezone-naive."""
    if is_naive(dt):
        return dt
    tzinfo = tz or get_default_timezone()
    if isinstance(dt, NepaliDateTime):
        gregorian_dt = dt.to_datetime()
        naive_dt = timezone.make_naive(gregorian_dt, tzinfo)
        return NepaliDateTime.from_datetime(naive_dt)
    return NepaliDateTime.from_datetime(timezone.make_naive(dt, tzinfo))


def now():
    """Return current NepaliDateTime."""
    return NepaliDateTime.now()


def timedelta(**kwargs):
    """Return a standard timedelta for use with NepaliDateTime."""
    return dt_timedelta(**kwargs)
