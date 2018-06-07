from django.contrib import admin

# Register your models here.
from .models import Task,Job,Answers,AssignedTaskSet

admin.site.register(Task)
admin.site.register(Job)
admin.site.register(Answers)
admin.site.register(AssignedTaskSet)
