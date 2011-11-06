from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User


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
    username = forms.RegexField(label="Username",
                                max_length=30,
                                regex=r'^[\w.@+-]+$',
                                help_text="30 characters or fewer. Letters, "
                                           "digits and @/./+/-/_ only",
                                error_messages={'invalid':
                                    "This value may contain only letters, "
                                    "numbers and @/./+/-/_ characters."})
    email = forms.EmailField(label="Email")

    def __init__(self, user, *args, **kwargs):
        self.user = user
        kwargs['initial'] = {'username': self.user.username,
                            'email': self.user.email}
        super(ProfileForm, self).__init__(user, *args, **kwargs)

    # Blatantly stolen from django.contrib.auth.forms
    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            "A user with that username already exists.")

    def save(self):
        if self.cleaned_data['new_password1']:
            super(ProfileForm, self).save(commit=False)
        self.user.username = self.cleaned_data['username']
        self.user.email = self.cleaned_data['email']
        self.user.save()
