

from django.conf.urls import url
from . import views

from .views import (
        post_delete,
        )
urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^(?P<menu_id>[0-9]+)/$', views.detail, name='detail'),
    
    url(r'^(?P<menu_id>[0-9]+)/results/$', views.results, name='results'),
 
     url(r'^post/$', views.post, name='update'),
     
     url(r'^post/(?P<pk>\d+)/$', views.detail, name='detail'),


    


]
