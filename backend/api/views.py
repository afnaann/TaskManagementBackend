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
        print(request.data)
        print(request.data['username'])
        print(request.data['password'])
        print(request.data['email'])
        subject = 'You Can now login to Task Management!'
        message = (
            f"Dear {request.data['username']},\n\n"
            "Thank you for registering with Task Management. Your account has been successfully created.\n\n"
            "You can now log in to the app using the following credentials:\n"
            f"Username: {request.data['username']}\n"
            f"Password: {request.data['password']}\n\n"
            "We recommend keeping your credentials safe and secure. If you have any questions, feel free to reach out to our support team.\n\n"
            "Best regards,\n"
            "The Task Management Team"
        )
        recipient_list= [serializer.data['email']]
        send_mail(subject,message,EMAIL_HOST_USER,recipient_list,fail_silently=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
