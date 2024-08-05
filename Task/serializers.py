from .models import Task
from Authentication.serializers import UserSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
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

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        
        # Update assigned_to_id
        assigned_to_id = validated_data.get('assigned_to_id')
        if assigned_to_id:
            assigned_to = User.objects.filter(id=assigned_to_id).first()
            if assigned_to:
                instance.assigned_to = assigned_to
            else:
                raise serializers.ValidationError({"assigned_to_id": "Assigned user does not exist."})
        
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.save()
        return instance



