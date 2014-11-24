from django import forms
from django.contrib.auth.models import User
import models
import time


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'username', 'password')


class PayForm(forms.ModelForm):
	amount = forms.IntegerField(label = 'Amount')
	description = forms.CharField(max_length=50, label = 'Description')
	
	class Meta:
		model = models.PaymentLog
		fields = ('amount', 'description')

class MakeGroupForm(forms.ModelForm):
	name = forms.CharField(max_length=20, label = 'Group Name')
        description = forms.CharField(max_length=50, label = 'Group Description', widget=forms.TextInput(attrs={'size':'37'}))
	passcode = forms.CharField(max_length=16, label = 'Group Passcode',widget=forms.PasswordInput())

	class Meta:
		model = models.PayGroup
		fields = ('name', 'description', 'passcode')

		


	
