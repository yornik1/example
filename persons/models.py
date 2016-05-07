from django.db import models

from django.contrib.auth.models import User

class Person(models.Model):
    short_name = models.CharField(max_length=32, unique=True, null=False,
                                    blank=False)
    full_name = models.CharField(max_length=128, null=True, blank=True)
    email = models.EmailField(max_length=128, null=True, blank=True)

    def __str__(self):
        return '%s%s' % (self.short_name,
                          ' (%s)' % self.full_name if self.full_name else '')

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
