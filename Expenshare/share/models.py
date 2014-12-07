##
# @file models.py
# @brief Contains the database models implemented by ExpenShare.
# @authors Taylor Andrews, Ian Char, Brennan McConnell
# @date 11/26/2014
# @note The __unicode__ function allows the models to communicate with Django admin.
#

from django.db import models
from django.contrib.auth.models import User
import time

##
# @class FellowUser
# @brief Model designed to represent a fellow group member for a single particular MemberView.
# @details FellowUser models interact with a MemberView model in order to represent the MemberView's
#          balances which they owe their fellow group members.
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
# @brief The MemberView model is designed to represent a single group member's view of the expense
#        balances.
# @details MemberView represents a particular viewpoint of the expenses. Many FellowUsers are
#          associated with a single Memberview. The MemberView then represents how much the
#          particular member owes his or her fellow group members. It is a look at the current
#          balance owed to all members from the viewpoint of a particular group member.
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
# @brief Model designed to represent a transaction.
# @details The PaymentLog model is used by a PayUser when he or she wants to report an Expense.
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
# @brief Model for an ExpenShare group.
# @details PayGroup is a model designed to represent one expense sharing group. It
# is associated with multiple members and contains a MemberView model per member which
# represents a members particular view point of the expenses incurred.
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
# @brief A model for a user of ExpenShare. A PayUser can join PayGroups and make PaymentLogs.
# @details A PayUser corresponds to both a User and a PayGroup and links them together.
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

