from django.conf.urls import url
from . import views

app_name = 'restaurant';
urlpatterns = [
    url(r'^$', views.home, name='home'),
	url(r'^guest-user/$', views.TableIDVerification, name='Guest User'),
	url(r'^order/$', views.ordernow, name='OrderNow'),
    url(r'^gateway/(\w+)/$', views.gateway, name='gateway'),
    url(r'^server/$', views.StartOrder, name='server'),
    url(r'^server/orders$', views.OrderView.as_view(), name='orders'),
    url(r'^server/(?P<pk>[0-9]+)/orderdetails$', views.OrderDetailView.as_view(), name='orderdetails'),
    url(r'^kitchen/$', views.KitchenView.as_view(), name='kitchen'),
    url(r'^kitchen/(?P<pk>[0-9]+)/kitchendetails$', views.KitchenDetailView.as_view(), name='kitchendetail'),

]
