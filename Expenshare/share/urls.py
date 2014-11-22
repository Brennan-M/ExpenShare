from django.conf.urls import patterns, url
import views

urlpatterns = patterns(' ',
	url(r'^$', views.index, name='index'),
	url(r'^home/$', views.home, name='home'),
	url(r'^history/$', views.history, name='history'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.userLogin, name='login'),
	url(r'^logout/$', views.userLogout, name='logout'))
