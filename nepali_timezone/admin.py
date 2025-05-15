"""
Admin integration for Nepali datetime fields.
"""

from django.contrib import admin
from django import forms
from .datetime import NepaliDateTime
from .formatters import format_nepali_datetime

class NepaliDateTimeAdminWidget(forms.widgets.DateTimeInput):
    """Admin widget for NepaliDateTime."""
    class Media:
        js = ("nepali_timezone/js/nepali_datetime.js",)
        css = {"all": ("nepali_timezone/css/nepali_datetime.css",)}

    def render(self, name, value, attrs=None, renderer=None):
        if isinstance(value, NepaliDateTime):
            value = format_nepali_datetime(value, format_type="%Y-%m-%d %H:%M:%S")
        return super().render(name, value, attrs, renderer)