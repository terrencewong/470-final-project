from django.conf.urls import url
from . import views

<<<<<<< HEAD
app_name = 'restaurant'
urlpatterns = [
    url(r'^$', views.home, name='home'),
	url(r'^guest-user/$', views.TableIDVerification, name='Guest User'),
	url(r'^guest-user/tryagain$', views.TryAgain, name='tryagain'),
	url(r'^order-placed/$', views.orderplaced, name='OrderPlaced'),
	url(r'^contact-server/$', views.ContactServer, name='ContactServer'),
	url(r'^contact-server-sent/$', views.ContactServerSent, name='ContactServerSent'),
=======
app_name = 'restaurant';
urlpatterns = [
    url(r'^$', views.home, name='home'),
	url(r'^guest-user/$', views.TableIDVerification, name='Guest User'),
	url(r'^order/$', views.ordernow, name='OrderNow'),
>>>>>>> caca943b08e3c9846d830490d7045b695ad02803
    url(r'^server/$', views.ServerView.as_view(), name='server'),
    url(r'^server/orderstart$', views.StartOrder, name='orderstart'),
    url(r'^gateway/(\w+)/$', views.gateway, name='gateway'),
    url(r'^server/orders$', views.OrderView.as_view(), name='orders'),
<<<<<<< HEAD
    url(r'^server/(?P<order_id>[0-9]+)/orderdetails$', views.orderdetail, name='orderdetails'),
=======
    url(r'^server/(?P<pk>[0-9]+)/orderdetails$', views.OrderDetailView.as_view(), name='orderdetails'),
>>>>>>> caca943b08e3c9846d830490d7045b695ad02803
    url(r'^server/(?P<pk>[0-9]+)/alertdetails$', views.AlertDetailView.as_view(), name='alertdetails'),
    url(r'^(?P<alert_id>[0-9]+)/resolveAlert/$', views.resolveAlert, name='resolveAlert'),
    url(r'^kitchen/$', views.KitchenView.as_view(), name='kitchen'),
    url(r'^kitchen/kitchendetail/(?P<order_id>[0-9]+)$', views.kitchendetail, name='kitchendetail'),
<<<<<<< HEAD
	
	url(r'^order-menu/$', views.MenuView.as_view(), name='Menu'),
	url(r'^(?P<pk>[0-9]+)/additem/$', views.AddItem, name='additem'),
	url(r'^login/$', views.login_view, name='Login'),
	url(r'^server/$', views.StartOrder, name='server'),
	url(r'^server/orders$', views.OrderView.as_view(), name='orders'),
	url(r'^server/(?P<pk>[0-9]+)/orderdetails$', views.OrderDetailView.as_view(), name='orderdetails'),
    url(r'^createaccount/$', views.createaccount),
    url(r'^payment/$', views.payment, name='payment'),
=======
>>>>>>> caca943b08e3c9846d830490d7045b695ad02803
]
