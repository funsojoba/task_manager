from .models import Task
from Authentication.serializers import UserSerializer
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Task
        fields = "__all__"


class CreateTaskSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField(required=False)
    status = serializers.ChoiceField(choices=Task.STATUS)
    assigned_to_id = serializers.CharField(required=False)
    due_date = serializers.DateTimeField()


class UpdateTaskSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    status = serializers.ChoiceField(choices=Task.STATUS, required=False)
    assigned_to_id = serializers.CharField(required=False)
    due_date = serializers.DateTimeField(required=False)



