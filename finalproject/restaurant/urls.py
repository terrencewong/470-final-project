from django.conf.urls import url

from . import views

app_name = 'restaurant';
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^server/$', views.StartOrder, name='server'),
]
