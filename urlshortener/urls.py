from django.conf.urls import include, url
from django.contrib import admin
from urlshortenerapp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^urlshortener/', include('urlshortenerapp.urls')),
    url(r'', views.redirect, name='redirect'),
]
