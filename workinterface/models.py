from django.db import models

# Create your models here.

from django.conf import settings


class JobManager(models.Manager):
    def get_keywords(self):
        keywords = [u.lower() for u in self.values_list('task_keywords',flat=True)]
        out = []
        for key in keywords:
            for token in key.split(','):
                token = token.strip(' ')
                if token not in out:
                    out.append(token)
        return out


class Job(models.Model):
    task_time = models.IntegerField()
    task_payment = models.DecimalField(decimal_places=2, max_digits=5)
    task_description = models.CharField(max_length=400,blank=True)
    task_title = models.CharField(max_length=255,blank=True)
    task_keywords = models.TextField(blank=True)

    objects = JobManager()


class Task(models.Model):
    task_type = models.ForeignKey(Job,on_delete=models.CASCADE)
    task_content = models.TextField()
    task_uid = models.PositiveIntegerField(unique=True)
    task_answer_content = models.TextField()

    def __str__(self):
        return "Task uid:{0} - {1}".format(self.task_uid,self.task_type.task_title)


class Answers(models.Model):
    task = models.ForeignKey(Task,on_delete=models.CASCADE)
    worker = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return "Task uid:{0} - Worker:{1} - Answer:{2}".format(self.task.task_uid,self.worker,self.content)
