from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import TaskSerializer, UserSerializer, UserTaskSerializer, UserGetSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from backend.settings import EMAIL_HOST_USER
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
from .models import Task,UserTasks
from django.db.models import Q
from django.contrib.auth.models import User

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
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

@permission_classes([IsAuthenticated])
class getTasks(APIView):
    def get(self,request):
        obj = Task.objects.all()
        serializer = TaskSerializer(obj,many=True)
        return Response(serializer.data)
    
@permission_classes([IsAuthenticated])
class userDashboard(APIView):
    def get(self,request):
        usertasks = UserTasks.objects.filter(user=request.user)
        serializer = UserTaskSerializer(usertasks,many=True)
        return Response(serializer.data)
    
@permission_classes([IsAuthenticated])
class allUserTasks(APIView):
    def get(self,request):
        tasks = UserTasks.objects.all()
        serializer = UserTaskSerializer(tasks,many=True)
        return Response(serializer.data)
        
@permission_classes([IsAuthenticated])
class submitTask(APIView):
    def post(self,request):
        title = request.data.get('title')
        print(title)
        
        task = Task.objects.filter(title=title).first()
        print(task)
        
        usertask = UserTasks.objects.select_related('task','user').filter(task=task,user=request.user).first()
        
        if usertask:
            print('happy')
            usertask.completed = True
            usertask.save()
            return Response({'Message':'Task marked as Completed!'})
        return Response({'Error':'Task marking error!'})
    
@permission_classes([IsAuthenticated])
class getUsers(APIView):
    def get(self,request):
        users = User.objects.filter(is_staff=False)
        serializer = UserGetSerializer(users, many=True)
        return Response(serializer.data)