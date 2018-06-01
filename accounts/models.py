from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.contrib.postgres.fields import ArrayField
from django.db.models import  Max, Count, F, Avg, Sum, Q


# Create your models here.

class User(AbstractUser):

    email = models.EmailField("Email")
    preference = ArrayField(models.CharField(max_length=255),null=True)
    age = models.PositiveIntegerField(null=True)
    education = models.CharField("Level of education",max_length=4,choices=[
        ('BS',"Bachelor's degree"),
        ('MS',"Master's degree"),
        ('PHD',"Doctorate"),
        ('PROF', "Higher level of Education"),
    ],null=True)
    nationality = CountryField(blank_label='(select country)',null=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("detail", kwargs={"username": self.username})

    @staticmethod
    def worker_info(worker):
        """Static method to retrieve worker's statistical information.
        @requires:  user - Instance from the User Django model.
        @returns:   One JSON array
        """
        query = User.objects.filter(username=worker).annotate(
            completed_task=Count('workertaskhistorymodel'),
            success_task=Count('workertaskhistorymodel', filter=Q(workertaskhistorymodel__successful__exact=True)),
            average_income=Avg('workertaskhistorymodel__task__task_type__task_payment',
                               filter=Q(workertaskhistorymodel__successful__exact=True)),
            max_income=Max('workertaskhistorymodel__task__task_type__task_payment',
                           filter=Q(workertaskhistorymodel__successful__exact=True)),
            sum_income=Sum('workertaskhistorymodel__task__task_type__task_payment',
                           filter=Q(workertaskhistorymodel__successful__exact=True)),
            sum_duration=Sum('workertaskhistorymodel__time_it_took',
                             filter=Q(workertaskhistorymodel__successful__exact=True)),
            avg_duration=Avg('workertaskhistorymodel__time_it_took',
                             filter=Q(workertaskhistorymodel__successful__exact=True)),
        )
        return query


