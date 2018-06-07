from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(WorkerModel)
admin.site.register(WorkerTaskHistoryModel)
admin.site.register(WorkerModelHistoryModel)
admin.site.register(TaskFeatureMapping)
admin.site.register(TaskFeaturesModel)
admin.site.register(WorkerPreferenceHistoryModel)
