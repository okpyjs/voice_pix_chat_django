from chat.models import TestModel
from rest_framework import serializers


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestModel
        fields = ["id", "name", "count"]
