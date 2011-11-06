from django import forms
from django.contrib.auth.forms import UserCreationForm

from models import WaitingList


class WaitingListForm(forms.ModelForm):
    class Meta:
        model = WaitingList
        fields = ('email',)


class RegistrationForm(UserCreationForm):
    #override the old awful password field
    password2 = forms.CharField(label="Confirmation",
                                widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email',)
