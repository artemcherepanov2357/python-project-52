from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username')
        labels = {
            'first_name': _('First name'),
            'last_name': _('Last name'),
            'username': _('Username'),
        }


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')
        labels = {
            'first_name': _('First name'),
            'last_name': _('Last name'),
            'username': _('Username'),
        }

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Username"),
        widget=forms.TextInput(attrs={'autofocus': True}),
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        strip=False,
    )