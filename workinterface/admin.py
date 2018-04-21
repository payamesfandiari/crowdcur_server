from django.contrib import admin

# Register your models here.
from .models import Task,Job,Answers

admin.site.register(Task)
admin.site.register(Job)
admin.site.register(Answers)