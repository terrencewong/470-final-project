from django.conf.urls import url

from . import views

app_name = 'restaurant';
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^server/$', views.StartOrder, name='server'),
    url(r'^server/orders$', views.OrderView.as_view(), name='orders'),
    url(r'^server/(?P<pk>[0-9]+)/orderdetails$', views.OrderDetailView.as_view(), name='orderdetails'),
]
