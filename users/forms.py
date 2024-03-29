from django import forms
from django.contrib.auth.models import UnicodeUsernameValidator

from .models import User


class UserRegistrationForm(forms.Form):

    full_name = forms.CharField(max_length=100, required=True)

    username = forms.CharField(
        max_length=150,
        help_text='REQUIRED',
        validators=[UnicodeUsernameValidator()],
        required=True
    )

    email = forms.EmailField(required=True)

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean_username(self):

        username = self.cleaned_data.get('username')
       # if len(username < 4):
        #    raise forms.ValidationError('username must at least be 4 characters long')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('username already exists')
        return username

    def clean_email(self):

        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists')
        return email

    def clean_password2(self):

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        # At least 8 char long
        if len(password1) < 8:
            raise forms.ValidationError("The new password must be at least 8 characters long." )
        # check for digit
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError('Password must contain at least 1 digit.')
        # check for letter
        if not any(char.isalpha() for char in password1):
            raise forms.ValidationError('Password must contain at least 1 letter.')
        # passwords should match
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2


class UserLoginForm(forms.Form):

    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class UserProfileUpdateForm(forms.Form):

    full_name = forms.CharField(max_length=100)

    username = forms.CharField(
        max_length=150,
        help_text='REQUIRED',
        validators=[UnicodeUsernameValidator()],
        required=True
    )

    email = forms.EmailField(required=True)

    avatar = forms.ImageField(label='Profile Pic', required=False)

    bio = forms.CharField(max_length=200, required=False,
                          widget=forms.Textarea(attrs={'cols': 40, 'rows': 3}))