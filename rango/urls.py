from django.conf.urls import patterns, url
from rango import views

urlpatterns = [
        url(r'^$', views.index, name='index'), # name is actually optional
        url(r'^about/', views.about, name='about')
]
