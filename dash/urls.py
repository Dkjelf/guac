from django.conf.urls import patterns, url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^profile/$', views.get_user_profile, name='profile'),
	url(r'^about/$', views.about, name='about'),
]

