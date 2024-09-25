from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
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
    
# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(required=True)
#     password = serializers.CharField(write_only=True, required=True)
    
#     def validate(self,data):
#         username = data.get('username')
#         password = data.get('password')
        
#         try:
#             user = User.objects.get(username=username)
#         except user.DoesNotExist:
#             raise serializers.ValidationError('User Does Not Exist')
#         user = authenticate(username=username,password=password)