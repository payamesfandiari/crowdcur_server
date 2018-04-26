from django.urls import path,re_path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(),name='work'),
    path('test_json/', views.json_test),
    path('<int:pk>/',views.DetailView.as_view(),name='answer'),
    path('<int:pk>/ans/',views.ans,name='sendans')
]

