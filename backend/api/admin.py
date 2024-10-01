from django.contrib import admin
from .models import Task, UserTasks
# Register your models here.

admin.site.register(Task)
admin.site.register(UserTasks)