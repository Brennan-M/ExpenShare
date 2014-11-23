from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
import time

# Django 1.7 has its own built in group thing so probably actually do not need this.
# That being said it needs additional things in it so we will create a new model


class PaymentLog(models.Model):
	#Django should create unique primary key already
	amount = models.IntegerField(default=0)
	description = models.CharField(max_length=400, default="")
	date = models.DateField(default=time.strftime("%Y-%m-%d"))
	user = models.ForeignKey(User)
	contested = models.BooleanField(default=False)
	contestedMessage = models.CharField(max_length=140, default="")

	#For other features may need...
	# contested : boolean, contestedMessage : CharField
	def __unicode__(self):
		return self.description

class PayGroup(models.Model):
	#Django should create unique primary key already
	name = models.CharField(max_length=20, default="")
	description = models.CharField(max_length=400, default="")
	members = models.ManyToManyField(User)
	passcode = models.CharField(max_length=16, default="") #This may need to be hashed
	paymentLogs = models.ManyToManyField(PaymentLog)
	#Should find out how to do owners later

	def __unicode__(self):
		return self.name

class PayUser(models.Model):
	userKey = models.ForeignKey(User)
	payGroups = models.ManyToManyField(PayGroup)

	def __unicode__(self):
		return self.userKey.username

