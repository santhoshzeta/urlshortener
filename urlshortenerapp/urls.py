from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    url(r'^shorten/$', views.shorten, name='shorten'),
    url(r'^topdomains/$', views.topdomains, name='topdomains'),
    url(r'^last100urls/$', views.last100urls, name='last100urls'),
    url(r'^urlvisitstats/$', views.urlvisitstats, name='urlvisitstats'),
    url(r'^retrievestats/$', views.retrievestats, name='retrievestats'),
]
