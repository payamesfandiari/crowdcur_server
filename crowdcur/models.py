from datetime import datetime
from django.db import models
from django.conf import settings
from django.contrib.postgres import fields
from estimators.models import Estimator
from accounts.models import User
from workinterface.models import Task
# Create your models here.


class TaskFeatureMapping(models.Model):
    feature_name = models.CharField(max_length=255)
    col_number = models.PositiveIntegerField()


class TaskFeaturesModel(models.Model):
    task = models.OneToOneField(to=Task,on_delete=models.CASCADE)
    feature = fields.JSONField()

    def __str__(self):
        return "Task uid:{0} - {1}".format(self.task.task_uid,self.feature)


class WorkerModel(models.Model):
    worker = models.OneToOneField(User,on_delete=models.CASCADE)
    worker_model = fields.JSONField(default={})
    needs_update = models.BooleanField(default=True)
    creation_time = models.DateTimeField(default=datetime.now)
    score = models.FloatField(default=0.0)

    def __str__(self):
        return "Worker:{0} - Model:{1} - Update?:{2} - Score:{3}".format(self.worker,
                                                                         self.worker_model,self.needs_update,self.score)


class WorkerTaskHistoryModel(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task,on_delete=models.CASCADE)
    time_it_took = models.FloatField(default=0.0)
    successful = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Worker:{0} - Task:{1} - Time:{2} - scuccessful?:{3}".format(self.worker,
                                                                         self.task,self.time_it_took,self.successful)


class WorkerPreferenceHistoryModel(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE)
    preference = fields.JSONField(blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    number_of_tasks_done = models.PositiveIntegerField(null=True)


class WorkerModelHistoryModel(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE)
    worker_model = fields.JSONField(default={})
    timestamp = models.DateTimeField(auto_now_add=True)


class WorkerKFactor(models.Model):
    worker = models.OneToOneField(User, on_delete=models.CASCADE)
    factors = fields.JSONField(null=True)


class PreferenceToFeaturesModel(models.Model):
    pref_name = models.CharField(blank=False,max_length=200)
    feature_number = models.PositiveIntegerField(blank=False)
