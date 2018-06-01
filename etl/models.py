from django.db import models
from accounts.models import User
from workinterface.models import Task,Job
from django.contrib.postgres import fields
from crowdcur.models import *
# Create your models here.


class SimilarWorkersBasedOnModel(models.Model):
    worker = models.ForeignKey(User,on_delete=models.CASCADE)
    similar_workers = fields.JSONField()


class FactTable(models.Model):
    task_title = models.CharField(max_length=500)
    task_requester = models.CharField(max_length=999)
    task_payment = models.FloatField()
    time_it_took = models.FloatField()
    age = models.PositiveIntegerField()
    education = models.CharField("Level of education", max_length=4, choices=[
        ('BS', "Bachelor's degree"),
        ('MS', "Master's degree"),
        ('PHD', "Doctorate"),
        ('PROF', "Higher level of Education"),
    ])
    nationality = models.CharField(max_length=4)
    day = models.PositiveIntegerField()
    hour = models.PositiveIntegerField()
