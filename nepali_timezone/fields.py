"""
Field classes for integration with frameworks like Django.
"""

from django.db import models
from django.utils import timezone
from django import forms
from .datetime import NepaliDateTime
from .utils import get_default_timezone
import nepali_datetime

class NepaliDateTimeInput(forms.DateTimeInput):
    """Custom widget for Nepali datetime input using nepali-date-picker."""
    input_type = "nepali-datetime"
    template_name = "nepali_timezone/widgets/nepali_datetime.html"

    class Media:
        css = {
            "all": ("nepali_timezone/css/nepali_datetime.css",)
        }
        js = (
            "nepali_timezone/js/nepali_datetime.js",
            "nepali_timezone/js/init.js",
        )

    def get_context(self, name, value, attrs):
        if isinstance(value, NepaliDateTime):
            value = value._nepali_dt.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(value, str):
            try:
                parts = value.split("-")
                if len(parts) >= 3:
                    year, month, day = (int(parts[0]), int(parts[1]), int(parts[2].split()[0]))
                    nepali_datetime.datetime(year, month, day)
            except (ValueError, TypeError, IndexError):
                value = None
        context = super().get_context(name, value, attrs)
        context["widget"]["attrs"]["class"] = "nepali-datetime-input"
        return context

class NepaliDateTimeFormField(forms.Field):
    """Form field for NepaliDateTime with admin widget."""
    widget = NepaliDateTimeInput

    def to_python(self, value):
        if value in self.empty_values:
            return None
        if isinstance(value, NepaliDateTime):
            return value
        try:
            from dateutil.parser import parse
            dt = parse(value)
            if dt.tzinfo is None:
                dt = timezone.make_aware(dt, get_default_timezone())
            return NepaliDateTime.from_datetime(dt)
        except (ValueError, TypeError):
            raise forms.ValidationError("Invalid datetime format", code="invalid")

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs["class"] = "nepali-datetime-input"
        return attrs

class NepaliDateTimeField(models.Field):
    """A model field for storing Nepali datetime, with auto_now and auto_now_add."""
    description = "A timezone-aware Nepali datetime field"

    def __init__(self, auto_now=False, auto_now_add=False, *args, **kwargs):
        self.auto_now = auto_now
        self.auto_now_add = auto_now_add
        if auto_now or auto_now_add:
            kwargs["editable"] = False
            kwargs["blank"] = True
        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        return "timestamp with time zone"

    def get_internal_type(self):
        return "DateTimeField"

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return NepaliDateTime.from_datetime(value)

    def to_python(self, value):
        if isinstance(value, NepaliDateTime):
            return value
        if value is None:
            return value
        if isinstance(value, str):
            try:
                from dateutil.parser import parse
                value = parse(value)
            except (ValueError, TypeError):
                raise forms.ValidationError("Invalid datetime format", code="invalid")
        return NepaliDateTime.from_datetime(value)

    def get_prep_value(self, value):
        if value is None:
            return None
        if isinstance(value, NepaliDateTime):
            return value.to_datetime()
        return timezone.make_aware(value, get_default_timezone())

    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            value = NepaliDateTime.now()
            setattr(model_instance, self.attname, value)
            return value.to_datetime()
        return super().pre_save(model_instance, add)

    def formfield(self, **kwargs):
        defaults = {"form_class": NepaliDateTimeFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)