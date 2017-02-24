from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^article/(?P<page>[0-9]+)/$', views.articleDetail, name='article detail'),
    url(r'^sources/$', views.sourceDetail, name='source detail'),
]
