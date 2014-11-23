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
	description = forms.CharField(max_length=200, label = 'Description')

	class Meta:
		model = models.PaymentLog
		fields = ('amount', 'description')

	