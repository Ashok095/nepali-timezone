"""
Formatters for Nepali dates and times.
"""

from .datetime import NepaliDateTime

NEPALI_MONTHS = {
    1: "Baisakh", 2: "Jestha", 3: "Asar", 4: "Shrawan",
    5: "Bhadra", 6: "Aswin", 7: "Kartik", 8: "Mangsir",
    9: "Poush", 10: "Magh", 11: "Falgun", 12: "Chaitra"
}

NEPALI_NUMERALS = {
    "0": "०", "1": "१", "2": "२", "3": "३", "4": "४",
    "5": "५", "6": "६", "7": "७", "8": "८", "9": "९"
}

def to_nepali_numerals(text):
    """Convert digits to Nepali numerals."""
    return "".join(NEPALI_NUMERALS.get(char, char) for char in str(text))

def format_nepali_datetime(dt, format_type="full", use_nepali_numerals=False):
    """Format Nepali datetime with month names and optional Nepali numerals."""
    if not isinstance(dt, NepaliDateTime):
        dt = NepaliDateTime.from_datetime(dt)
    
    if format_type == "full":
        formatted = f"{NEPALI_MONTHS[dt.month]} {dt.day}, {dt.year} {dt.hour:02d}:{dt.minute:02d} {dt.tzinfo.tzname(None)}"
    elif format_type == "date":
        formatted = f"{NEPALI_MONTHS[dt.month]} {dt.day}, {dt.year}"
    else:
        formatted = dt._nepali_dt.strftime(format_type or "%Y-%m-%d %H:%M:%S")
    
    if use_nepali_numerals:
        formatted = to_nepali_numerals(formatted)
    return formatted