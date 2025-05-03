from rest_framework import serializers
from ..models import SubTask


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = ['id', 'title', 'is_done', 'task', 'created_at']