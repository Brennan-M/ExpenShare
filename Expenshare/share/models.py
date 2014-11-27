##
# @file models.py
# @brief django models for ExpenShare
# @authors Taylor Andrews, Ian Char, Brennan McConnell
# @date 11/26/2014
# @note the __unicode__ function allows the models to communicate with Django admin
#

from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
import time

##
# @class FellowUser
# @brief django model for fellow user in a group
#
class FellowUser(models.Model):
	user = models.ForeignKey(User)
	owed = models.DecimalField(max_digits=11, decimal_places=2, default=0)

	##
	# @brief gets model's information in unicode string format
	# @return the fellow user's username
	#
	def __unicode__(self):
		return self.user.username

##
# @class MemberView
# @brief django model for viewing the members in a group
#
class MemberView(models.Model):
	user = models.ForeignKey(User)
	netOwed = models.DecimalField(max_digits=11, decimal_places=2, default=0)
	fellows = models.ManyToManyField(FellowUser)
	
	##
	# @brief gets model's information in unicode string format
	# @return the member's username
	#
	def __unicode__(self):
		return self.user.username

##
# @class PaymentLog
# @brief django model for the payment log as entered by an user
#
class PaymentLog(models.Model):
	#Django should create unique primary key already
	amount = models.DecimalField(max_digits=11, decimal_places=2, default=0)
	description = models.CharField(max_length=50, default="")
	date = models.DateField(default=time.strftime("%Y-%m-%d"))
	user = models.ForeignKey(User)
	contested = models.BooleanField(default=False)
	contestedMessage = models.CharField(max_length=140, default="")

	##
	# @brief gets model's information in unicode string format
	# @return description of the payment log
	#
	def __unicode__(self):
		return self.description

##
# @class PayGroup
# @brief django model for a paygroup of users
#
class PayGroup(models.Model):
	#Django should create unique primary key already
	name = models.CharField(max_length=20, default="", unique=True)
	description = models.CharField(max_length=50, default="")
	members = models.ManyToManyField(User)
	passcode = models.CharField(max_length=16, default="") #This may need to be hashed
	paymentLogs = models.ManyToManyField(PaymentLog)
	memberViews = models.ManyToManyField(MemberView)
	groupSize = models.IntegerField(default=1)

	##
	# @brief gets model's information in unicode string format
	# @return the name of the paygroup 
	#
	def __unicode__(self):
		return self.name

##
# @class PayUser
# @brief a django model for an user which is a member of paygroups
#
class PayUser(models.Model):
	userKey = models.ForeignKey(User)
	payGroups = models.ManyToManyField(PayGroup)

	##
	# @brief gets model's information in unicode string format
	# @return the user's key
	#
	def __unicode__(self):
		return self.userKey.username

