import unittest
import sys
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Expenshare.settings')
import django
from django.test import TestCase
django.setup()
from share.models import User
from share.models import PayGroup
from share.models import PaymentLog
from share.models import PayUser
import time
import share.forms
import share.views
from subprocess import call

# To Test our database, run python manage.py test
# This uses djangos test implmentation and creates a private database
class TestExpenShare(TestCase):

	def setUp(self):
		self.ian = User(username="Ian")
		self.bren = User(username="Brennan")
		self.ian.save()
		self.bren.save()
		self.ianP = PayUser(userKey=self.ian)
		self.brenP = PayUser(userKey=self.bren)
		self.ianP.save()
		self.brenP.save()
		self.pg1 = PayGroup(name="Group 1", description="Group for all users", passcode="1234")
		self.pg2 = PayGroup(name="Group 2", description="Group for Ian, Brennan", passcode="1234")
		self.pg3 = PayGroup(name="Group 3", description="NullGroup", passcode="1234")
		self.pg1.save()
		self.pg2.save()
		self.pg3.save()
		self.pg1.members.add(self.ianP.userKey)
		self.pg1.members.add(self.brenP.userKey)
		self.pg2.members.add(self.ianP.userKey)
		self.pg2.members.add(self.brenP.userKey)
		self.ianP.payGroups.add(self.pg1)
		self.ianP.payGroups.add(self.pg2)
		self.brenP.payGroups.add(self.pg1)
		self.brenP.payGroups.add(self.pg2)
		self.pl1 = PaymentLog(amount=10, description="Bought some eggs", user=self.ianP.userKey)
		self.pl2 = PaymentLog(amount=20, description="Bought gas", user=self.brenP.userKey)
		self.pl1.save()
		self.pl2.save()

	def test_PayUser_with_PayGroup(self):
		self.assertEqual(self.pg1 in self.brenP.payGroups.all(), True)
		self.assertEqual(self.pg3 in self.ianP.payGroups.all(), False)
		self.assertEqual(self.ian in self.pg2.members.all(), True)
		self.pg1.members.remove(self.brenP.userKey)
		self.brenP.payGroups.remove(self.pg1)
		self.assertEqual(self.pg1 in self.brenP.payGroups.all(), False)
		self.assertEqual(self.bren in self.pg1.members.all(), False)

	def test_PaymentLog_with_PayGroup(self):
		self.assertEqual(self.pl2 in self.pg2.paymentLogs.all(), False)
		self.pg2.paymentLogs.add(self.pl2)
		self.assertEqual(self.pl2 in self.pg2.paymentLogs.all(), True)




if __name__ == '__main__':
	unittest.main()
