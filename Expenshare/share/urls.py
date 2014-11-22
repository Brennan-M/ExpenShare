from django.conf.urls import patterns, url
from share import views

urlpatterns = patterns(' ',
	url(r'^$', views.index, name='index'),
	url(r'^home/$', views.home, name='home'),
	url(r'^history/$', views.history, name='history'),
	url(r'^register/$', views.register, name='register'),
	url(r'^add_payform/$', views.add_payform, name='add_payform'),
	url(r'^login/$', views.userLogin, name='login'),
	url(r'^logout/$', views.userLogout, name='logout'))

