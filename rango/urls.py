from django.conf.urls import url
from rango import views

urlpatterns = [
        url(r'^$', views.index, name='index'), # name is actually optional
        url(r'^about/$', views.about, name='about'),
        url(r'^add_category/$', views.add_category, name='add_category'),
        # make sure the parameter matches what's specified in views.py
        url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
        url(r'^category/(?P<slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
]
