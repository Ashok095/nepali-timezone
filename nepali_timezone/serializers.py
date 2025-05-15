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
        # Validate format string compatibility with nepali_datetime
        self._validate_format_string(self.format)
        super().__init__(*args, **kwargs)

    def _validate_format_string(self, format_str):
        """Validate that the format string is compatible with nepali_datetime."""
        # List of format codes known to be supported by nepali_datetime
        supported_codes = [
            "%Y",
            "%m",
            "%d",
            "%H",
            "%M",
            "%S",
            "%f",
            "%y",
            "%b",
            "%B",
            "%a",
            "%A",
            "%I",
            "%p",
        ]

        # Simple validation - check if any unsupported codes are used
        for i, char in enumerate(format_str):
            if char == "%" and i + 1 < len(format_str):
                code = "%" + format_str[i + 1]
                if code not in supported_codes and format_str[i + 1] not in "Z":
                    # Z is handled separately for timezone
                    raise ValueError(
                        f"Format code {code} may not be supported by nepali_datetime"
                    )

    def to_representation(self, value):
        if value is None:
            return None

        if not isinstance(value, NepaliDateTime):
            try:
                value = NepaliDateTime.from_datetime(value)
            except (ValueError, TypeError):
                return None

        try:
            # Handle %Z separately if needed
            if "%Z" in self.format:
                base_format = self.format.replace("%Z", "")
                formatted = value._nepali_dt.strftime(base_format)
                return formatted + value.tzinfo.tzname(None)
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
