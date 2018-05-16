from django.urls import path, re_path
from . import views,api

urlpatterns = [
    path('plugin_api/send_answer', views.log_worker_answer),
    path('plugin_api/set_tasks', views.set_worker_shown_tasks),
    path('plugin_api/get_info', views.get_info),
    path('get_feedback/', views.WorkerFeedbackView.as_view(), name='feedback'),
    path('dashboard/', views.WorkerDashboardView.as_view(), name='dashboard'),
    path('dashboard/get_task_type', views.get_task_type),
    path('dashboard/get_income', views.get_income),
    path('dashboard/get_time_spent', api.get_time_spent,name='get_time_spent'),
    path('dashboard/get_accuracy', views.get_accuracy),
]
