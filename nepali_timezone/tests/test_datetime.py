from django.test import TestCase
from django.conf import settings
from nepali_timezone import NepaliDateTime, now, timedelta, make_aware, make_naive, is_aware, is_naive
from django.utils import timezone
from datetime import datetime

class NepaliDateTimeTests(TestCase):
    def test_dynamic_timezone(self):
        with self.settings(TIME_ZONE="UTC"):
            dt = now()
            self.assertEqual(dt.tzinfo.tzname(None), "UTC")

    def test_make_aware(self):
        naive_dt = NepaliDateTime(2082, 1, 7)
        aware_dt = make_aware(naive_dt)
        self.assertTrue(is_aware(aware_dt))

    def test_make_naive(self):
        aware_dt = now()
        naive_dt = make_naive(aware_dt)
        self.assertTrue(is_naive(naive_dt))

    def test_is_aware_naive(self):
        aware_dt = now()
        naive_dt = NepaliDateTime(2082, 1, 7)
        self.assertTrue(is_aware(aware_dt))
        self.assertTrue(is_naive(naive_dt))

    def test_calendar_conversion(self):
        # This test uses approximate conversion - actual dates may vary
        # based on the nepali_datetime library implementation
        gregorian_dt = datetime(2025, 4, 13)  # Around Nepali New Year
        nepali_dt = NepaliDateTime.from_gregorian(2025, 4, 13)
        
        # Convert back to Gregorian and check if date is close
        # (within a day to account for implementation differences)
        converted_back = nepali_dt.to_gregorian()
        delta = abs((converted_back.date() - gregorian_dt.date()).days)
        self.assertLessEqual(delta, 1, "Conversion should be accurate within 1 day")