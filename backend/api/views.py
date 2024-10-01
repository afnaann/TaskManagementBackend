from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import TaskSerializer, UserSerializer, UserTaskSerializer, UserGetSerializer, UserTasksIdSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from backend.settings import EMAIL_HOST_USER
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny,IsAdminUser
from rest_framework.views import APIView
from .models import Task,UserTasks
from django.db.models import Q
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

@api_view(['POST'])
@permission_classes([IsAdminUser])
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

class getTasks(APIView):
    def get(self,request):
        obj = Task.objects.all()
        serializer = TaskSerializer(obj,many=True)
        return Response(serializer.data)
    
class userDashboard(APIView):
    def get(self,request):
        usertasks = UserTasks.objects.filter(user=request.user)
        serializer = UserTaskSerializer(usertasks,many=True)
        return Response(serializer.data)
    
class allUserTasks(APIView):
    def get(self,request):
        tasks = UserTasks.objects.all()
        serializer = UserTaskSerializer(tasks,many=True)
        return Response(serializer.data)
        
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
    
class getUsers(APIView):
    def get(self,request):
        users = User.objects.filter(is_staff=False)
        serializer = UserGetSerializer(users, many=True)
        return Response(serializer.data)
    

class addTask(APIView):
    def post(self,request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            task = Task.objects.create(title=serializer.validated_data['title'],description=serializer.validated_data['description'])
            return Response(serializer.data)
        return Response({'msg':'Error Adding Task.'})
    
class assignTask(APIView):
    def post(self,request):
        task = Task.objects.get(title=request.data['task'])        
        assignees = request.data.get('assignees',[])
        user_emails = [assignee['value'] for assignee in assignees]
        users = User.objects.filter(email__in=user_emails)
        
        for user in users:
            data = {
                'task': task.id,
                'user':user.id,
                'completed':False
            }
            serializer = UserTasksIdSerializer(data=data)
            
            if serializer.is_valid():
                serializer.save()
                pass
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg':'created'},status=status.HTTP_201_CREATED)