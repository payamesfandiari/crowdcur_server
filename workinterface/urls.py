from django.urls import path,re_path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(),name='work'),
    path('<int:pk>/',views.DetailView.as_view(),name='answer'),
    path('refresh/',views.refresh_workspace,name='refresh'),
    path('<int:pk>/ans/',views.ans,name='sendans')
]

