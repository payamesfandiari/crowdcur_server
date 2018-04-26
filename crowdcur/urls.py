from django.urls import path,re_path
from . import views

urlpatterns = [
    path('plugin_api/sendanswer',views.log_worker_answer),
]

