from datetime import datetime
from django.db import models
from django.conf import settings
from django.contrib.postgres import fields
from estimators.models import Estimator
from accounts.models import User
from workinterface.models import Task
# Create your models here.


class TaskFeaturesModel(models.Model):
    task_uid = models.OneToOneField(to=Task,on_delete=models.CASCADE,to_field='task_uid')
    task_feature = fields.ArrayField(models.FloatField())


class WorkerModel(models.Model):
    worker = models.OneToOneField(User,on_delete=models.CASCADE)
    worker_model = models.OneToOneField(Estimator,on_delete=models.CASCADE)
    needs_update = models.BooleanField(default=True)
    creation_time = models.DateTimeField(default=datetime.now)
    score = models.FloatField(default=0.0)


class WorkerTaskHistoryModel(models.Model):
    worker = models.OneToOneField(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task,on_delete=models.CASCADE)


class WorkerPreferenceHistoryModel(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE)
    preference = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class WorkerKFactor(models.Model):
    worker = models.OneToOneField(User, on_delete=models.CASCADE)
    factors = fields.JSONField()
