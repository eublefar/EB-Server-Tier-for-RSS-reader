from django.conf.urls import url

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^register/$', views.register_page, name="register"),
    url(r'^login/$', views.login_view ,name="login"),
    url(r'^logout/$', views.logout_page, name="logout"),
    url(r'^$', views.main_page, name="main page"),
    url(r'^profile/(?P<pk>[0-9]+)/$', views.edit_user, name='user_profile_edit')
]
