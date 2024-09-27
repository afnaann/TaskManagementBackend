from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    file = models.FileField(blank=True,null=True)
    
class AssignTasks(models.Model):
    task = models.ForeignKey(Task,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    completed = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.task.title}"



