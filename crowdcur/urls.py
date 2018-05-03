from django.urls import path,re_path
from . import views

urlpatterns = [
    path('plugin_api/send_answer',views.log_worker_answer),
    path('plugin_api/set_tasks',views.set_worker_shown_tasks),
    path('plugin_api/get_info',views.get_info),
    path('get_feedback/',views.WorkerFeedbackView.as_view(),name='feedback'),
    path('dashboard/',views.WorkerDashboardView.as_view()),
]

