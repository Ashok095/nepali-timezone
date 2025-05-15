# Nepali Timezone

A Django package for timezone-aware Nepali (Bikram Sambat) datetime support, mirroring Django's timezone functionality.

## Installation

```bash
pip install nepali-timezone
```

## Features

- Timezone-aware Nepali datetime handling
- Django model fields for Nepali dates
- DRF serializer fields
- Admin integration
- Form fields with Nepali date picker

## Usage

### Basic Usage

```python
from nepali_timezone import NepaliDateTime, now

# Get current Nepali datetime
current = now()
print(current)  # 2080-01-01 12:30:45 Asia/Kathmandu

# Create a specific Nepali date
nepali_date = NepaliDateTime(2080, 1, 1)

# Convert from Gregorian to Nepali
from datetime import datetime
gregorian_date = datetime(2023, 4, 14)
nepali_date = NepaliDateTime.from_datetime(gregorian_date)
```

### Django Models

```python
from django.db import models
from nepali_timezone import NepaliDateTimeField

class Event(models.Model):
    title = models.CharField(max_length=100)
    nepali_date = NepaliDateTimeField()
    created_at = NepaliDateTimeField(auto_now_add=True)
```

### DRF Serializers

```python
from rest_framework import serializers
from nepali_timezone import NepaliDateTimeSerializerField

class EventSerializer(serializers.ModelSerializer):
    nepali_date = NepaliDateTimeSerializerField()
    
    class Meta:
        model = Event
        fields = ['id', 'title', 'nepali_date']
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.