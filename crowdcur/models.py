from datetime import datetime
from django.db import models
from django.conf import settings

from estimators.models import Estimator
from accounts.models import User
# Create your models here.



class TaskFeatures(models.Model):
    pass


class WorkerModel(models.Model):
    worker = models.OneToOneField(User,on_delete=models.CASCADE)
    worker_model = models.OneToOneField(Estimator,on_delete=models.CASCADE)
    needs_update = models.BooleanField(default=True)
    creation_time = models.DateTimeField(default=datetime.now)


class WorkerPreferenceHistory(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE)
    preference = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
# class WorkerDoneTasks(models.Model):
#     pass
