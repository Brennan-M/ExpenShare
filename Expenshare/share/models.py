from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
import time

# Django 1.7 has its own built in group thing so probably actually do not need this.
# That being said it needs additional things in it so we will create a new model
class FellowUser(models.Model):
	user = models.ForeignKey(User)
	owed = models.DecimalField(max_digits=11, decimal_places=2, default=0)

	def __unicode__(self):
		return self.user.username

class MemberView(models.Model):
	user = models.ForeignKey(User)
	netOwed = models.DecimalField(max_digits=11, decimal_places=2, default=0)
	fellows = models.ManyToManyField(FellowUser)

	def __unicode__(self):
		return self.user.username

class PaymentLog(models.Model):
	#Django should create unique primary key already
	amount = models.DecimalField(max_digits=11, decimal_places=2, default=0)
	description = models.CharField(max_length=50, default="")
	date = models.DateField(default=time.strftime("%Y-%m-%d"))
	user = models.ForeignKey(User)
	contested = models.BooleanField(default=False)
	contestedMessage = models.CharField(max_length=140, default="")

	def __unicode__(self):
		return self.description

class PayGroup(models.Model):
	#Django should create unique primary key already
	name = models.CharField(max_length=20, default="", unique=True)
	description = models.CharField(max_length=50, default="")
	members = models.ManyToManyField(User)
	passcode = models.CharField(max_length=16, default="") #This may need to be hashed
	paymentLogs = models.ManyToManyField(PaymentLog)
	memberViews = models.ManyToManyField(MemberView)
	groupSize = models.IntegerField(default=1)
	#Should find out how to do owners later

	def __unicode__(self):
		return self.name

class PayUser(models.Model):
	userKey = models.ForeignKey(User)
	payGroups = models.ManyToManyField(PayGroup)

	def __unicode__(self):
		return self.userKey.username

