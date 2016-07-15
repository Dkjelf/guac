from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	# Links UserProfile to a User model instance
	user = models.OneToOneField(User)
	# The additional attributes we wish to include.
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	picture = models.ImageField(upload_to='profile_images', blank=True)
	isAdmin = models.BooleanField(default=False)

	# Override the __unicode__() method to return out something actually meaningful
	def __unicode__(self):
		return self.user.username
