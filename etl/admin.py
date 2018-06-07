from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(FactTable)
admin.site.register(ETLHistory)
admin.site.register(SimilarWorkersBasedOnModel)