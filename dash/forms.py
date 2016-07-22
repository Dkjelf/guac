from dash.models import UserProfile
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate
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
class LoginForm(forms.Form):
	username = forms.CharField(max_length=255, required=True)
	password = forms.CharField(widget=forms.PasswordInput, required=True)

	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		if not user or not user.is_active:
			raise forms.ValidationError("That login was invalid. Please try again.")
		return self.cleaned_data

	def login(self, request):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		return user
