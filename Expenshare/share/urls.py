from django.conf.urls import patterns, url
import views

urlpatterns = patterns(' ',
	url(r'^$', views.index, name='index'),
	url(r'^home/$', views.home, views.post_transaction('POST', 20, 'Practice'), name='home'),
	url(r'^history/$', views.history, name='history'))
