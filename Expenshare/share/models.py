##
# @file models.py
# @brief Django models for ExpenShare
# @authors Taylor Andrews, Ian Char, Brennan McConnell
# @date 11/26/2014
# @note The __unicode__ function allows the models to communicate with Django admin.
#

from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
import time

##
# @class FellowUser
# @brief Django model for determining which users share groups
# @details Django model fellow user interacts with memberview to represent the memberviews balances which they owe their fellow group members.
#
class FellowUser(models.Model):
	user = models.ForeignKey(User)
	owed = models.DecimalField(max_digits=11, decimal_places=2, default=0)

	##
	# @brief Gets model's information in unicode string format
	# @return The fellow user's username
	#
	def __unicode__(self):
		return self.user.username

##
# @class MemberView
# @brief Django model for viewing the members in a group
# @details MemberView uses FellowUser to determine who else is in a particular group. 
#
class MemberView(models.Model):
	user = models.ForeignKey(User)
	netOwed = models.DecimalField(max_digits=11, decimal_places=2, default=0)
	fellows = models.ManyToManyField(FellowUser)
	
	##
	# @brief Gets model's information in unicode string format
	# @return The member's username
	#
	def __unicode__(self):
		return self.user.username

##
# @class PaymentLog
# @brief Django model for the payment log as entered by an user
# @details PaymentLog relies on an User to record payment information. Allows for contesting payment ammounts.
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
	# @brief Gets model's information in unicode string format
	# @return Description of the payment log
	#
	def __unicode__(self):
		return self.description

##
# @class PayGroup
# @brief Django model for a paygroup of users
# @details PayGroup interacts with both PaymentLog and MemberView to determin what payments are owed between which users. 
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
	# @brief Gets model's information in unicode string format
	# @return The name of the paygroup 
	#
	def __unicode__(self):
		return self.name

##
# @class PayUser
# @brief A django model for an user which is a member of paygroups
# @details A PayUser corresponds to both an User and a PayGroup, it links them together. 
#
class PayUser(models.Model):
	userKey = models.ForeignKey(User)
	payGroups = models.ManyToManyField(PayGroup)

	##
	# @brief Gets model's information in unicode string format
	# @return The user's key
	#
	def __unicode__(self):
		return self.userKey.username

