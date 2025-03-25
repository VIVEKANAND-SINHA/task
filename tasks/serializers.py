from rest_framework import serializers
from .models import Task, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile']

class TaskSerializer(serializers.ModelSerializer):
    assigned_user = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'

class TaskSerializerUserWise(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'


