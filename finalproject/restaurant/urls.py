from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^welcome/$', views.welcome, name='Welcome'),
	url(r'^guest-user/$', views.TableIDVerification, name='Guest User'),
	url(r'^order/$', views.ordernow, name='OrderNow'),
]
