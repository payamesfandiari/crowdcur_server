from django.urls import path,re_path
from workinterface import views

urlpatterns = [
    path('', views.IndexView.as_view(),name='index'),
    path('<int:pk>/',views.DetailView.as_view(),name='answer'),
    path('<int:pk>/ans/',views.ans,name='sendans')
]
