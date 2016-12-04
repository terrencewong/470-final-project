from django.conf.urls import url
from . import views

app_name = 'restaurant';
urlpatterns = [
    url(r'^$', views.home, name='home'),
	url(r'^guest-user/$', views.TableIDVerification, name='Guest User'),
	url(r'^order/$', views.ordernow, name='OrderNow'),
    url(r'^server/$', views.ServerView.as_view(), name='server'),
    url(r'^server/orderstart$', views.StartOrder, name='orderstart'),
    url(r'^gateway/(\w+)/$', views.gateway, name='gateway'),
    url(r'^server/orders$', views.OrderView.as_view(), name='orders'),
    url(r'^server/(?P<pk>[0-9]+)/orderdetails$', views.OrderDetailView.as_view(), name='orderdetails'),
    url(r'^server/(?P<pk>[0-9]+)/alertdetails$', views.AlertDetailView.as_view(), name='alertdetails'),
    url(r'^(?P<alert_id>[0-9]+)/resolveAlert/$', views.resolveAlert, name='resolveAlert'),
    url(r'^kitchen/$', views.KitchenView.as_view(), name='kitchen'),
    url(r'^kitchen/kitchendetail/(?P<order_id>[0-9]+)$', views.kitchendetail, name='kitchendetail'),
]
