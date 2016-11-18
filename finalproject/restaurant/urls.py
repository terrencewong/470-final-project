from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^kitchen/$', views.KitchenView.as_view(), name='kitchen'),
    url(r'^kitchen/(?P<pk>[0-9]+)/kitchendetails$', views.KitchenDetailView.as_view(), name='kitchendetail'),
]
