from django.test import TestCase
from rest_framework import serializers
from nepali_timezone import NepaliDateTimeField, NepaliDateTime
from .test_fields import TestModel

class TestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestModel
        fields = ["created", "updated"]

class NepaliSerializerTests(TestCase):
    def test_auto_serialize(self):
        instance = TestModel.objects.create()
        serializer = TestModelSerializer(instance)
        data = serializer.data
        self.assertIn("2082", data["created"])  # Approx BS year
        self.assertTrue(data["updated"])  # Ensure updated is serialized

    def test_read_only_auto_now(self):
        serializer = TestModelSerializer(data={"created": "2082-01-07 12:00:00 Asia/Kathmandu", "updated": "2082-01-07 12:00:00 Asia/Kathmandu"})
        self.assertTrue(serializer.is_valid())
        self.assertNotIn("updated", serializer.validated_data)  # auto_now is read-only