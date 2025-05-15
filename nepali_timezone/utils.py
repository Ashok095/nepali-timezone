"""
Utility functions for Nepali date and time operations.
"""

from django.conf import settings
import pytz
from datetime import timedelta

class NepalTimeZone(pytz.tzfile.DstTzInfo):
    """Timezone class for Nepal Standard Time (NST, UTC+05:45)."""
    def __init__(self):
        self._utcoffset = timedelta(hours=5, minutes=45)
        self._tzname = "Asia/Kathmandu"
        self.zone = "Asia/Kathmandu"

    def utcoffset(self, dt):
        return self._utcoffset

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return self._tzname

    def localize(self, dt, is_dst=False):
        if dt.tzinfo is not None:
            raise ValueError("Cannot localize a datetime with existing timezone")
        return dt.replace(tzinfo=self)
    
    def fromutc(self, dt):
        """Convert UTC datetime to local time."""
        if dt.tzinfo is None:
            raise ValueError("fromutc() requires a non-naive datetime")
        return dt.replace(tzinfo=self) + self._utcoffset

def get_default_timezone():
    """Return the timezone from settings.TIME_ZONE, defaulting to NepalTimeZone."""
    try:
        return pytz.timezone(getattr(settings, "TIME_ZONE", "Asia/Kathmandu"))
    except pytz.exceptions.UnknownTimeZoneError:
        return NepalTimeZone()