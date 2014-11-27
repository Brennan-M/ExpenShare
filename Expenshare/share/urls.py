##
# @file urls.py
# @brief URL map for ExpenShare
# @authors Taylor Andrews, Ian Char, Brennan McConnell
# @date 11/25/2014
# @details The urlpatterns uses regular expressions to match urls and pass them to views.
#

from django.conf.urls import patterns, url
from share import views

##
# Contains all the url tuples for the ExpenShare website.
#
urlpatterns = patterns(' ',
	url(r'^$', views.index, name='index'),
	url(r'^home/$', views.home, name='home'),
	url(r'^history/$', views.history, name='history'),
	url(r'^register/$', views.register, name='register'),
	url(r'^add_payform/$', views.add_payform, name='add_payform'),
	url(r'^add_groupform/$', views.add_groupform, name='add_groupform'),
	url(r'^joingroup_form/$', views.joingroup_form, name='joingroup_form'),
	url(r'^removePayForm/$', views.removePayForm, name='removePayForm'),
	url(r'^leavegroup/$', views.leavegroup, name='leavegroup'),
	url(r'^login/$', views.userLogin, name='login'),
	url(r'^logout/$', views.userLogout, name='logout'),
	url(r'^confirmPayment/$', views.confirmPayment, name='confirmPayment'))
