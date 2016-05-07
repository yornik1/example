from django.contrib import admin
from persons.models import Person, UserProfile

admin.site.register(Person)
admin.site.register(UserProfile)
