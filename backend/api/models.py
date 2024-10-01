from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    file = models.FileField(upload_to='folders/',blank=True,null=True)
    all_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    
class UserTasks(models.Model):
    task = models.ForeignKey(Task,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.task.title}"



