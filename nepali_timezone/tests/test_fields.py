from django.test import TestCase
from django.db import models
from nepali_timezone import NepaliDateTimeField, NepaliDateTime
from django import forms

class TestModel(models.Model):
    created = NepaliDateTimeField(auto_now_add=True)
    updated = NepaliDateTimeField(auto_now=True)

    class Meta:
        app_label = "nepali_timezone"

class NepaliDateTimeFieldTests(TestCase):
    def test_auto_now_add(self):
        instance = TestModel.objects.create()
        self.assertIsInstance(instance.created, NepaliDateTime)
        self.assertIsNotNone(instance.created)

    def test_auto_now(self):
        instance = TestModel.objects.create()
        original_updated = instance.updated
        instance.save()
        self.assertNotEqual(instance.updated, original_updated)

    def test_formfield(self):
        field = TestModel._meta.get_field("created")
        form_field = field.formfield()
        self.assertIsInstance(form_field, forms.Field)
        self.assertEqual(form_field.widget.attrs["class"], "nepali-datetime-input")