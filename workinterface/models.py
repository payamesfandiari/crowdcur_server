from django.db import models

# Create your models here.

from django.conf import settings


class Job(models.Model):
    task_time = models.IntegerField()
    task_payment = models.DecimalField(decimal_places=2, max_digits=5)
    task_description = models.CharField(max_length=400,blank=True)
    task_title = models.CharField(max_length=255,blank=True)
    task_keywords = models.TextField(blank=True)


class Task(models.Model):
    task_type = models.ForeignKey(Job,on_delete=models.CASCADE)
    task_content = models.TextField()
    task_uid = models.PositiveIntegerField(unique=True)
    task_answer_content = models.TextField()

    def __str__(self):
        return "Task uid:"+str(self.id)+"-"+ str(self.task_uid)


class Answers(models.Model):
    task = models.ForeignKey(Task,on_delete=models.CASCADE)
    worker = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return "Task uid:"+str(self.task_id)+"-"+ str(self.worker_id)
