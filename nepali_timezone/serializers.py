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
        if not isinstance(value, NepaliDateTime):
            value = NepaliDateTime.from_datetime(value)
        return value._nepali_dt.strftime(self.format)

    def to_internal_value(self, data):
        from dateutil.parser import parse
        try:
            dt = parse(data)
            if dt.tzinfo is None:
                dt = timezone.make_aware(dt, get_default_timezone())
            return NepaliDateTime.from_datetime(dt)
        except ValueError:
            raise serializers.ValidationError("Invalid datetime format")

# Register NepaliDateTimeField for ModelSerializer
serializers.ModelSerializer.serializer_field_mapping[NepaliDateTimeModelField] = NepaliDateTimeField