from django import forms
from django.contrib.auth.forms import PasswordChangeForm


class ProfileForm(PasswordChangeForm):
    #Make password fields optional
    new_password1 = forms.CharField(label="New password",
                                    widget=forms.PasswordInput,
                                    required=False,
                                    help_text="Optional")
    new_password2 = forms.CharField(label="Confirm password",
                                    widget=forms.PasswordInput,
                                    required=False,
                                    help_text="Optional")
    username = forms.CharField(label="Username")
    email = forms.EmailField(label="Email")

    def __init__(self, user, *args, **kwargs):
        self.user = user
        kwargs['initial'] = {'username': self.user.username,
                            'email': self.user.email}
        super(ProfileForm, self).__init__(user, *args, **kwargs)

    def save(self):
        if self.cleaned_data['new_password1']:
            super(ProfileForm, self).save(commit=False)
        self.user.username = self.cleaned_data['username']
        self.user.email = self.cleaned_data['email']
        self.user.save()
