from django.urls import path,re_path
from showtasks import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('',views.api_root),
    path('snippets/', views.SnippetList.as_view(),name='snippet-list'),
    re_path(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view(),name='snippet-detail'),
    re_path(r'^snippets/(?P<pk>[0-9]+)/highlight/$', views.SnippetHighlight.as_view(),name='snippet-highlight'),
    path('users/',views.UserList.as_view(),name='user-list'),
    re_path(r'^users/(?P<pk>[0-9]+)/$',views.UserDetail.as_view(),name='user-detail'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
