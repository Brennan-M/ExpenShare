from django.db import models
from django.contrib.auth.models import Group
# Django 1.7 has its own built in group thing so probably actually do not need this.
# That being said it needs additional things in it so we will create a new model
class PayGroup(models.model):
	#Django should create unique primary key already
	name = OneToOneField(Group)
	description = models.CharField(max_length=400)
	members = ManyToManyField(User)

	def __unicode__(self):
		return self.name

class PaymentLog(models.model):
	#Django should create unique primary key already
	amount = models.IntegerField(default=0)
	description = models.CharField(max_length=400)
	date = models.DateField()
	group = models.ForeignKey(Group)
	user = models.ForeignKey(User)

	#For other features may need...
	# contested : boolean, contestedMessage : CharField
	def __unicode__(self):
		return self.name

