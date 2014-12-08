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
from django.test import Client
from django import forms

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
		client = Client()

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

	def test_register(self):
		response = self.client.post('/share/register/', {'email' : "testEmail@emails.test",
													'username' : "testUser",
													'password' : "secret"})
		self.assertEqual(response.status_code == 200, True)
		self.assertEqual(User.objects.filter(username="testUser").exists(), True)

	def test_register_nonUnique_error(self):
		response = self.client.post('/share/register/', {'email' : "testEmail@emails.test",
													'username' : "testUser",
													'password' : "secret"})
		response = self.client.post('/share/register/', {'email' : "testEmail@emails.test",
													'username' : "testUser",
													'password' : "secret"})
		self.assertNotEqual(User.objects.filter(username="testUser").count(), 2)

	def test_home_notLoggedIn_error(self):
		response = self.client.get('/share/home/')
		self.assertNotEqual(response.status_code, 200)

	def test_home_loggedIn(self):
		
		response = self.client.post('/share/register/', {'email' : "testEmail@emails.test",
														 'username' : "testUser",
														 'password' : "secret"})
		response = self.client.post('/share/login/', {'username' : "testUser",
												 	  'password' : "secret"})
		self.assertEqual(response.status_code, 302)
		response = self.client.get('/share/home/')
		self.assertEqual(response.status_code, 200)

	def test_makeGroup(self):
		self.client.post('/share/register/', {'email' : "testEmail@emails.test",
														 'username' : "testUser",
														 'password' : "secret"})
		self.client.post('/share/login/', {'username' : "testUser",
									 	   'password' : "secret"})
		response = self.client.post('/share/add_groupform/', {'name' : "New Group",
															  'description': "a new group",
															  'passcode' : "secret"})
		self.assertEqual(response.status_code, 200)
		self.assertEqual(PayGroup.objects.filter(name = "New Group").exists(), True)
		added = False
		for member in PayGroup.objects.get(name = "New Group").members.all():
			if member.username == "testUser":
				added = True
		self.assertEqual(added, True)

	def test_makeGroup_nonUnique_error(self):
		self.client.post('/share/register/', {'email' : "testEmail@emails.test",
														 'username' : "testUser",
														 'password' : "secret"})
		self.client.post('/share/login/', {'username' : "testUser",
									 	   'password' : "secret"})
		self.client.post('/share/add_groupform/', {'name' : "New Group",
												   'description': "a new group",
												   'passcode' : "secret"})
		request = self.client.post('/share/add_groupform/', {'name' : "New Group",
												   'description': "a new group",
												   'passcode' : "secret"})
		self.assertEqual(request.status_code, 200)
		self.assertEqual(PayGroup.objects.filter(name = "New Group").count(), 1)

	def test_joinGroup(self):
		self.client.post('/share/register/', {'email' : "testEmail@emails.test",
														 'username' : "testUser",
														 'password' : "secret"})
		self.client.post('/share/login/', {'username' : "testUser",
									 	   'password' : "secret"})
		testPG = PayGroup(name = "Test Group", description = "test", passcode = "secret")
		testPG.save()
		response = self.client.post('/share/joingroup_form/', {'group': "Test Group",
															 'passcode' : "secret"})
		self.assertEqual(response.status_code, 200)
		added = False
		for member in testPG.members.all():
			if member.username == "testUser":
				added = True
		self.assertEqual(added, True)
		added = False
		for member_view in testPG.memberViews.all():
			if member_view.user.username == "testUser":
				added = True
		self.assertEqual(added, True)

	def test_joinGroup_alreadyJoined_error(self):
		self.client.post('/share/register/', {'email' : "testEmail@emails.test",
														 'username' : "testUser",
														 'password' : "secret"})
		self.client.post('/share/login/', {'username' : "testUser",
									 	   'password' : "secret"})
		testPG = PayGroup(name = "Test Group", description = "test", passcode = "secret")
		testPG.save()
		self.client.post('/share/joingroup_form/', {'group': "Test Group",
													'passcode' : "secret"})
		response = self.client.post('/share/joingroup_form/', {'group': "Test Group",
															 'passcode' : "secret"})
		self.assertEqual(response.status_code, 200)
		timesAdded = 0
		for member in testPG.members.all():
			if member.username == "testUser":
				timesAdded += 1
		self.assertEqual(timesAdded, 1)
		timesAdded = 0
		for member_view in testPG.memberViews.all():
			if member_view.user.username == "testUser":
				timesAdded = 1
		self.assertEqual(timesAdded, 1)


	def test_joinGroup_noGroup_error(self):
		self.client.post('/share/register/', {'email' : "testEmail@emails.test",
														 'username' : "testUser",
														 'password' : "secret"})
		self.client.post('/share/login/', {'username' : "testUser",
									 	   'password' : "secret"})
		response = self.client.post('/share/joingroup_form/', {'group' : "not exist",
															   'passcode' : 'secret'})
		self.assertEqual(response.status_code, 200)

	def test_joinGroup_multipleJoins(self):
		self.client.post('/share/register/', {'email' : "testEmail@emails.test",
														 'username' : "testUser",
														 'password' : "secret"})
		self.client.post('/share/login/', {'username' : "testUser",
									 	   'password' : "secret"})
		testPG = PayGroup(name = "Test Group", description = "test", passcode = "secret")
		testPG.save()
		self.client.post('/share/joingroup_form/', {'group': "Test Group",
													'passcode' : "secret"})
		self.client.post('/share/logout/')
		self.client.post('/share/register/', {'email' : "testEmail@emails.test",
											  'username' : "testUser2",
											  'password' : "secret"})
		self.client.post('/share/login/', {'username' : "testUser2",
									 	   'password' : "secret"})
		response = self.client.post('/share/joingroup_form/', {'group': "Test Group",
			   												   'passcode' : "secret"})
		
		self.assertEqual(response.status_code, 200)

		added = False
		for member in testPG.members.all():
			if member.username == "testUser":
				added = True
		self.assertEqual(added, True)

		added = False
		for member in testPG.members.all():
			if member.username == "testUser2":
				added = True
		self.assertEqual(added, True)

		added = False
		fellowAdded = False
		for member_view in testPG.memberViews.all():
			if member_view.user.username == "testUser":
				added = True
				for fellow in member_view.fellows.all():
					if fellow.user.username == "testUser2":
						fellowAdded = True
		self.assertEqual(added, True)
		self.assertEqual(fellowAdded, True)

		added = False
		fellowAdded = False
		for member_view in testPG.memberViews.all():
			if member_view.user.username == "testUser2":
				added = True
				for fellow in member_view.fellows.all():
					if fellow.user.username == "testUser":
						fellowAdded = True
		self.assertEqual(added, True)
		self.assertEqual(fellowAdded, True)

	def test_addPayment(self):
		self.client.post('/share/register/', {'email' : "testEmail@emails.test",
														 'username' : "testUser",
														 'password' : "secret"})
		self.client.post('/share/login/', {'username' : "testUser",
									 	   'password' : "secret"})
		testPG = PayGroup(name = "Test Group", description = "test", passcode = "secret", groupSize = 0)
		testPG.save()
		self.client.post('/share/joingroup_form/', {'group': "Test Group",
													'passcode' : "secret"})
		self.client.post('/share/logout/')
		self.client.post('/share/register/', {'email' : "testEmail@emails.test",
														 'username' : "testUser2",
														 'password' : "secret"})
		self.client.post('/share/login/', {'username' : "testUser2",
									 	   'password' : "secret"})
		self.client.post('/share/joingroup_form/', {'group': "Test Group",
   												    'passcode' : "secret"})
		request = self.client.post('/share/add_payform/', {'amount' : 10,
														   'description' : "test",
														   'group' : "Test Group"})
		added = False
		for payment in testPG.paymentLogs.all():
			added = payment.amount == 10
		self.assertEqual(added, True)

		correctAmounts = True
		for member_view in testPG.memberViews.all():
			if member_view.user.username == "testUser2":
				if member_view.netOwed != -5:
					correctAmounts = False
					for fellow in member_view.fellows.all():
						if fellow.owed != -5:
							correctAmounts = False
			else:
				if member_view.netOwed != 5:
					correctAmounts = False
					for fellow in member_view.fellows.all():
						if fellow.owed != 5:
							correctAmounts = False
		self.assertEqual(correctAmounts, True)

	def test_addPayment_invalidAmount_error(self):
		self.client.post('/share/register/', {'email' : "testEmail@emails.test",
														 'username' : "testUser",
														 'password' : "secret"})
		self.client.post('/share/login/', {'username' : "testUser",
									 	   'password' : "secret"})
		testPG = PayGroup(name = "Test Group", description = "test", passcode = "secret", groupSize = 0)
		testPG.save()
		self.client.post('/share/joingroup_form/', {'group': "Test Group",
													'passcode' : "secret"})
		self.client.post('/share/logout/')
		self.client.post('/share/register/', {'email' : "testEmail@emails.test",
														 'username' : "testUser2",
														 'password' : "secret"})
		self.client.post('/share/login/', {'username' : "testUser2",
									 	   'password' : "secret"})
		self.client.post('/share/joingroup_form/', {'group': "Test Group",
   												    'passcode' : "secret"})
		request = self.client.post('/share/add_payform/', {'amount' : "abcdef",
														   'description' : "test",
														   'group' : "Test Group"})
		self.assertEqual(request.status_code, 200)

		added = False
		for payment in testPG.paymentLogs.all():
			added = True
		self.assertEqual(added, False)

	def test_leaveGroup(self):
		self.client.post('/share/register/', {'email' : "testEmail@emails.test",
														 'username' : "testUser",
														 'password' : "secret"})
		self.client.post('/share/login/', {'username' : "testUser",
									 	   'password' : "secret"})
		testPG1 = PayGroup(name = "Test Group", description = "test", passcode = "secret", groupSize = 0)
		testPG1.save()
		testPG2 = PayGroup(name = "Test Group 2", description = "test", passcode = "secret", groupSize = 0)
		testPG2.save()
		self.client.post('/share/joingroup_form/', {'group': "Test Group",
													'passcode' : "secret"})
		self.client.post('/share/joingroup_form/', {'group': "Test Group 2",
													'passcode' : "secret"})
		self.client.post('/share/logout/')
		self.client.post('/share/register/', {'email' : "testEmail@emails.test",
														 'username' : "testUser2",
														 'password' : "secret"})
		self.client.post('/share/login/', {'username' : "testUser2",
									 	   'password' : "secret"})
		self.client.post('/share/joingroup_form/', {'group': "Test Group",
   												    'passcode' : "secret"})
		self.client.post('/share/joingroup_form/', {'group': "Test Group 2",
													'passcode' : "secret"})
		response = self.client.post('/share/leavegroup/', {'group' : "Test Group"})
		self.assertEqual(response.status_code, 200)
		
		removed = True
		for member in testPG1.members.all():
			if member.username == "testUser2":
				removed = False
		self.assertEqual(removed, True)

		removed = True
		for member_view in testPG1.memberViews.all():
			if member_view.user.username == "testUser2":
				removed = False
		self.assertEqual(removed, True)

		removed = True
		for member in testPG2.members.all():
			if member.username == "testUser2":
				removed = False
		self.assertNotEqual(removed, True)

		removed = True
		for member_view in testPG2.memberViews.all():
			if member_view.user.username == "testUser2":
				removed = False
		self.assertNotEqual(removed, True)

		self.client.post('/share/logout/')
		self.client.post('/share/login/', {'username' : "testUser",
									 	   'password' : "secret"})
		response = self.client.post('/share/leavegroup/', {'group' : "Test Group"})

		self.assertEqual(response.status_code, 200)

		removed = True
		for group in PayGroup.objects.all():
			if group.name == "Test Group":
				removed = False
		self.assertEqual(removed, True)

	def test_history(self):
		self.client.post('/share/register/', {'email' : "testEmail@emails.test",
														 'username' : "testUser",
														 'password' : "secret"})
		self.client.post('/share/login/', {'username' : "testUser",
									 	   'password' : "secret"})
		testPG = PayGroup(name = "Test Group", description = "test", passcode = "secret", groupSize = 0)
		testPG.save()
		self.client.post('/share/joingroup_form/', {'group': "Test Group",
													'passcode' : "secret"})
		response = self.client.post('/share/history', {'group' : "Test Group"})
		self.assertEqual(response.status_code, 301)

	def test_confirmPayment(self):
		self.client.post('/share/register/', {'email' : "testEmail@emails.test",
														 'username' : "testUser",
														 'password' : "secret"})
		self.client.post('/share/login/', {'username' : "testUser",
									 	   'password' : "secret"})
		testPG = PayGroup(name = "Test Group", description = "test", passcode = "secret", groupSize = 0)
		testPG.save()
		self.client.post('/share/joingroup_form/', {'group': "Test Group",
													'passcode' : "secret"})
		self.client.post('/share/logout/')
		self.client.post('/share/register/', {'email' : "testEmail@emails.test",
														 'username' : "testUser2",
														 'password' : "secret"})
		self.client.post('/share/login/', {'username' : "testUser2",
									 	   'password' : "secret"})
		self.client.post('/share/joingroup_form/', {'group': "Test Group",
   												    'passcode' : "secret"})
		self.client.post('/share/add_payform/', {'amount' : "10",
 											   	 'description' : "test",
											     'group' : "Test Group"})
		response = self.client.post('/share/confirmPayment/', {'group' : "Test Group",
															   'payAmount' : 3,
															   'target_member' : "testUser"})
		self.assertEqual(response.status_code, 200)

		correctAmounts = True
		for member_view in testPG.memberViews.all():
			if member_view.user.username == "testUser2":
				if member_view.netOwed != -2:
					correctAmounts = False
					for fellow in member_view.fellows.all():
						if fellow.owed != -2:
							correctAmounts = False
			else:
				if member_view.netOwed != 2:
					correctAmounts = False
					for fellow in member_view.fellows.all():
						if fellow.owed != 2:
							correctAmounts = False
		self.assertEqual(correctAmounts, True)

		response = self.client.post('/share/confirmPayment/', {'group' : "Test Group",
															   'payAmount' : 2,
															   'target_member' : "testUser"})

		correctAmounts = True
		for member_view in testPG.memberViews.all():
			if member_view.user.username == "testUser2":
				if member_view.netOwed != 0:
					correctAmounts = False
					for fellow in member_view.fellows.all():
						if fellow.owed != 0:
							correctAmounts = False
			else:
				if member_view.netOwed != 0:
					correctAmounts = False
					for fellow in member_view.fellows.all():
						if fellow.owed != 0:
							correctAmounts = False
		self.assertEqual(correctAmounts, True)

	def test_confirmPayment_invalidAmounts_error(self):
		self.client.post('/share/register/', {'email' : "testEmail@emails.test",
														 'username' : "testUser",
														 'password' : "secret"})
		self.client.post('/share/login/', {'username' : "testUser",
									 	   'password' : "secret"})
		testPG = PayGroup(name = "Test Group", description = "test", passcode = "secret", groupSize = 0)
		testPG.save()
		self.client.post('/share/joingroup_form/', {'group': "Test Group",
													'passcode' : "secret"})
		self.client.post('/share/logout/')
		self.client.post('/share/register/', {'email' : "testEmail@emails.test",
														 'username' : "testUser2",
														 'password' : "secret"})
		self.client.post('/share/login/', {'username' : "testUser2",
									 	   'password' : "secret"})
		self.client.post('/share/joingroup_form/', {'group': "Test Group",
   												    'passcode' : "secret"})
		self.client.post('/share/add_payform/', {'amount' : "10",
 											   	 'description' : "test",
											     'group' : "Test Group"})

		response = self.client.post('/share/confirmPayment/', {'group' : "Test Group",
															   'payAmount' : 11,
															   'target_member' : "testUser"})
		self.assertEqual(response.status_code, 200)

		correctAmounts = True
		for member_view in testPG.memberViews.all():
			if member_view.user.username == "testUser2":
				if member_view.netOwed != -5:
					correctAmounts = False
					for fellow in member_view.fellows.all():
						if fellow.owed != -5:
							correctAmounts = False
			else:
				if member_view.netOwed != 5:
					correctAmounts = False
					for fellow in member_view.fellows.all():
						if fellow.owed != 5:
							correctAmounts = False
		self.assertEqual(correctAmounts, True)

		response = self.client.post('/share/confirmPayment/', {'group' : "Test Group",
															   'payAmount' : "asdfds",
															   'target_member' : "testUser"})
		self.assertEqual(response.status_code, 200)

		correctAmounts = True
		for member_view in testPG.memberViews.all():
			if member_view.user.username == "testUser2":
				if member_view.netOwed != -5:
					correctAmounts = False
					for fellow in member_view.fellows.all():
						if fellow.owed != -5:
							correctAmounts = False
			else:
				if member_view.netOwed != 5:
					correctAmounts = False
					for fellow in member_view.fellows.all():
						if fellow.owed != 5:
							correctAmounts = False
		self.assertEqual(correctAmounts, True)

	def test_removePayment(self):
		self.client.post('/share/register/', {'email' : "testEmail@emails.test",
														 'username' : "testUser",
														 'password' : "secret"})
		self.client.post('/share/login/', {'username' : "testUser",
									 	   'password' : "secret"})
		testPG = PayGroup(name = "Test Group", description = "test", passcode = "secret", groupSize = 0)
		testPG.save()
		self.client.post('/share/joingroup_form/', {'group': "Test Group",
													'passcode' : "secret"})
		self.client.post('/share/logout/')
		self.client.post('/share/register/', {'email' : "testEmail@emails.test",
														 'username' : "testUser2",
														 'password' : "secret"})
		self.client.post('/share/login/', {'username' : "testUser2",
									 	   'password' : "secret"})
		self.client.post('/share/joingroup_form/', {'group': "Test Group",
   												    'passcode' : "secret"})
		self.client.post('/share/add_payform/', {'amount' : "10",
 											   	 'description' : "test",
											     'group' : "Test Group"})
		self.client.post('/share/add_payform/', {'amount' : "20",
 											   	 'description' : "test 2",
											     'group' : "Test Group"})
		for log in testPG.paymentLogs.all():
			if log.amount == 10:
				logID = log.id

		response = self.client.post('/share/removePayForm/', {'group' : "Test Group",
												  			  'log' : logID})
		self.assertEqual(response.status_code, 200)

		removed = True
		for payment in testPG.paymentLogs.all():
			if payment.amount == 10:
				removed = False
		self.assertEqual(removed, True)


	def test_removePayment_error(self):
		self.client.post('/share/register/', {'email' : "testEmail@emails.test",
														 'username' : "testUser",
														 'password' : "secret"})
		self.client.post('/share/login/', {'username' : "testUser",
									 	   'password' : "secret"})
		testPG = PayGroup(name = "Test Group", description = "test", passcode = "secret", groupSize = 0)
		testPG.save()
		self.client.post('/share/joingroup_form/', {'group': "Test Group",
													'passcode' : "secret"})
		self.client.post('/share/logout/')
		self.client.post('/share/register/', {'email' : "testEmail@emails.test",
														 'username' : "testUser2",
														 'password' : "secret"})
		self.client.post('/share/login/', {'username' : "testUser2",
									 	   'password' : "secret"})
		self.client.post('/share/joingroup_form/', {'group': "Test Group",
   												    'passcode' : "secret"})
		self.client.post('/share/add_payform/', {'amount' : "10",
 											   	 'description' : "test",
											     'group' : "Test Group"})
		self.client.post('/share/logout/')
		self.client.post('/share/login/', {'username' : "testUser",
									 	   'password' : "secret"})

		for log in testPG.paymentLogs.all():
			if log.amount == 10:
				logID = log.id

		response = self.client.post('/share/removePayForm/', {'group' : "Test Group",
												  			  'log' : logID})

		self.assertEqual(response.status_code, 200)

		removed = True
		for payment in testPG.paymentLogs.all():
			if payment.amount == 10:
				removed = False
		self.assertNotEqual(removed, True)




if __name__ == '__main__':
	unittest.main()