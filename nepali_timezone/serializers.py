"""
Serializers for Nepali date and time objects.
"""

from rest_framework import serializers
from .datetime import NepaliDateTime
from .utils import get_default_timezone
from django.utils import timezone
from .fields import NepaliDateTimeField as NepaliDateTimeModelField


class NepaliDateTimeField(serializers.Field):
    """Serializer field for NepaliDateTime."""

    def __init__(self, *args, **kwargs):
        self.format = kwargs.pop("format", "%Y-%m-%d %H:%M:%S %Z")
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        if value is None:
            return None

        if not isinstance(value, NepaliDateTime):
            try:
                value = NepaliDateTime.from_datetime(value)
            except (ValueError, TypeError):
                return None

        try:
            # Rely on nepali_datetime's strftime for all formatting
            else:
                return value._nepali_dt.strftime(self.format)
        except ValueError as e:
            # Log the error or handle it as appropriate
            return str(value)

    def to_internal_value(self, data):
        if data is None:
            return None

        from dateutil.parser import parse

        try:
            # Try to parse with timezone info preserved
            dt = parse(data)

            # If timezone info is present in the string, respect it
            if dt.tzinfo is not None:
                return NepaliDateTime.from_datetime(dt)
            else:
                # Otherwise use default timezone
                return NepaliDateTime.from_datetime(
                    timezone.make_aware(dt, get_default_timezone())
                )
        except (ValueError, TypeError):
            raise serializers.ValidationError("Invalid datetime format")


# Register NepaliDateTimeField for ModelSerializer
serializers.ModelSerializer.serializer_field_mapping[NepaliDateTimeModelField] = (
    NepaliDateTimeField
)
