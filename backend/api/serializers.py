from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Task, UserTasks
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['staff_status'] = user.is_staff
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','email','password']

    def validate_username(self, value):
        if not value.isalnum():
            raise serializers.ValidationError('Username should only contain alphanumeric characters!')
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters.')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists.')
        return value
    def create(self,validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields =  ['title','description','file','all_completed']
        
        

class UserTaskSerializer(serializers.ModelSerializer):
    task = TaskSerializer()
    user = UserSerializer()
    class Meta:
        model = UserTasks
        fields = ['task','user','completed']
        
class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email']
        
class UserTasksIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTasks
        fields = ['task','user','completed']