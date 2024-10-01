from django.urls import path

from .serializers import MyTokenObtainPairView
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import MyTokenObtainPairView
urlpatterns = [
    path('register/',views.register),
    
    path('api/login',MyTokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('api/login/refresh',TokenRefreshView.as_view(),name='token_refresh'),
    
    path('tasks/get',views.getTasks.as_view()), # Not Using Currently
    path('tasks/home',views.userDashboard.as_view()),
    path('tasks/submit',views.submitTask.as_view()),
    
    path('admin/getusers',views.getUsers.as_view()),
    path('admin/alltasks',views.allUserTasks.as_view()),
    path('admin/addtask',views.addTask.as_view()),
    path('admin/assigntask',views.assignTask.as_view())
]

