from dash.models import UserProfile
from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
	username = forms.CharField(help_text="Enter a username.")
	email = forms.CharField(help_text="Enter your email.")
	password = forms.CharField(widget=forms.PasswordInput(), help_text="Enter a password.")

	class Meta:
		model = User
		fields = ['username', 'email', 'password']
		
class UserProfileForm(forms.ModelForm):
	first = forms.CharField(help_text="Enter your first name.")
	last = forms.CharField(help_text="Enter your last name.")
	picture = forms.ImageField(help_text="Select a profile image", required=False)

	class Meta:
		model = UserProfile
		fields = ['first', 'last', 'picture']
 
