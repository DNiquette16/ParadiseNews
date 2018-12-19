from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class MyRegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True)
	firstName = forms.CharField(required=True)
	lastName = forms.CharField(required=True)
	class Meta:
		model = User
		fields = ('username', 'firstName','lastName','email', 'password1')
	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.firstName = self.cleaned_data['firstName']
		user.lastName = self.cleaned_data['lastName']
		user.email = self.cleaned_data['email']

		if commit:
			user.save()

		return user