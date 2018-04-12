from django.db import models

# Create your models here.


class Job(models.Model):
    task_time = models.IntegerField()
    task_payment = models.DecimalField(decimal_places=2, max_digits=5)
    task_description = models.CharField(max_length=400,blank=True)


class Task(models.Model):
    task_type = models.ForeignKey(Job,on_delete=models.CASCADE)
    task_content = models.TextField()
    task_uid = models.PositiveIntegerField()
    task_answer_content = models.TextField()

    def __str__(self):
        return "Task type:"+ str(self.task_type.task_description)


class Answers(models.Model):
    task = models.ForeignKey(Task,on_delete=models.CASCADE)
    worker = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    content = models.TextField()