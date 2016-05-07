from django import forms
from persons.models import UserProfile
from django.contrib.auth.models import User

class AddPersonForm(forms.Form):
    short_name = forms.CharField(max_length=32, required=True)
    full_name = forms.CharField(max_length=128, required=False)
    email = forms.EmailField(max_length=128, required=False)

class RemovePersonForm(forms.Form):
    short_name_substr = forms.CharField(max_length=32, required=True)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
