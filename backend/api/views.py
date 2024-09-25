from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from backend.settings import EMAIL_HOST_USER
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        print(serializer.data)
        print(serializer.data['username'])
        print(serializer.data['password'])
        print(serializer.data['email'])
        subject = 'You Can now login to Task Management!'
        message = f'Dear {serializer.data['username']}, You Have Successfully Registered into Task management. Now You can Login into App using Credentials, username: {serializer.data['username']}, Password: {serializer.data['password']}'
        recipient_list= [serializer.data['email']]
        send_mail(subject,message,EMAIL_HOST_USER,recipient_list,fail_silently=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
