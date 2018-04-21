from django.urls import path,re_path
from . import views

urlpatterns = [
    path('signup/', views.UserRegister.as_view(),name='signup'),
    path('profile/<username>',views.UserDetail.as_view(),name='profile')
]

