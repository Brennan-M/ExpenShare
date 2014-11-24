import unittest
import sys
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Expenshare.settings')
import django
django.setup()
import share.models
import time
import share.forms
import share.views
from subprocess import call



class TestExpenShare(unittest.TestCase):

    def setUp(self):
        self.ian = User(username="Ian")
		self.bren = User(username="Brennan")
		self.ian.save()
		self.bren.save()
		self.ianP = PayUser(userKey=ian)
		self.brenP = PayUser(userKey=bren)
		self.ian.save()
		self.bren.save()
		self.pg1 = PayGroup(name="Group 1", description="Group for all users", passcode="1234")
		self.pg2 = PayGroup(name="Group 2", description="Group for Ian, Brennan", passcode="1234")
		self.pg3 = PayGroup(name="Group 3", description="NullGroup", passcode="1234")
		self.pg1.save()
		self.pg2.save()
		self.pg3.save()
		self.pg1.members.add(ianP.userKey)
		self.pg1.members.add(brenP.userKey)
		self.pg2.members.add(ianP.userKey)
		self.pg2.members.add(brenP.userKey)
		self.ian.payGroups.add(pg1)
		self.ian.payGroups.add(pg2)
		self.bren.payGroups.add(pg1)
		self.bren.payGroups.add(pg2)
		self.pl1 = PaymentLog(amount=10, description="Bought some eggs", user=ianP.userKey)
		self.pl2 = PaymentLog(amount=20, description="Bought gas", user=brenP.userKey)
		self.pl1.save()
		self.pl2.save()

    def tearDown(self):
    	call(["python manage.py", "flush"])

    def checkUsers(self):



if __name__ == '__main__':
    unittest.main()