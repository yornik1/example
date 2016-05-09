from django.db import models
from django.contrib.auth.models import User
from sys import path
path.append('..')
from jobs.models import Job, FilteredJobsWrapper
from random import choice


class Person(models.Model):
    short_name = models.CharField(max_length=32, unique=True, null=False,
                                    blank=False)
    full_name = models.CharField(max_length=128, null=True, blank=True)
    email = models.EmailField(max_length=128, null=True, blank=True)
    code_job = models.CharField(max_length=128, null=True, blank=True)
    description = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return '%s%s%s' % (self.short_name,
                           ' (%s)' % self.full_name if self.full_name else '',
                           ' %s' % self.description)

    def update_jobs(self, code_digit_sum=8, random=False):
        job = choice(Job.objects.all())
        self.code_job = job.code_job
        self.description = job.description
        #self.save()
'''     if not random:
            for self in Person.objects.all():
                self.job = FilteredJobsWrapper(code_digit_sum)
                print('!', self.job.code_job)
                i.save()
        else:
            for i in Person.objects.all():
                random_person = choice(Person.objects.all())
                random_person.job = FilteredJobsWrapper(code_digit_sum)
'''





class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
