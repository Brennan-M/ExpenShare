##
# @file forms.py
# @brief django forms for taking input from ExpenShare users
# @authors Taylor Andrews, Ian Char, Brennan McConnell
# @date 11/26/2014
# @note django Meta class defines non-field aspects of django forms
#

from django import forms
from django.contrib.auth.models import User
import models
import time

##
# @class UserForm
# @brief a form for creating a user
# @details UserForm requires a password and username
#
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    ##
    # @brief meta defines corresponding model (User) and fields 
    #
    class Meta:
        model = User
        fields = ('email', 'username', 'password')

##
# @class PayForm
# @brief a form for entering a payment amount and description
#
class PayForm(forms.ModelForm):
	amount = forms.DecimalField(max_digits=11, decimal_places=2, label = 'Amount')
	description = forms.CharField(max_length=50, label = 'Description')
	
        ##
        # @brief meta defines corresponding model (PaymentLog) and fields 
        #
	class Meta:
		model = models.PaymentLog
		fields = ('amount', 'description')

##
# @class MakeGroupForm
# @brief a form for creating a group
# @details MakeGroupForm requires a group name, description, and passcode
#
class MakeGroupForm(forms.ModelForm):
	name = forms.CharField(max_length=20, label = 'Group Name')
	description = forms.CharField(max_length=50, label = 'Group Description', widget=forms.TextInput(attrs={'size':'37'}))
	passcode = forms.CharField(max_length=16, label = 'Group Passcode',widget=forms.PasswordInput())

        ##
        # @brief meta defines corresponding model (PayGroup) and fields 
     	#
	class Meta:
		model = models.PayGroup
		fields = ('name', 'description', 'passcode')

		


	
