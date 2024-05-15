from django import forms
from django.contrib.auth.models import User
from .models import Profile
from .tasks import send_review_email_task
class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password=forms.CharField(label='Parol',
                             widget=forms.PasswordInput)
    password_2=forms.CharField(label='Parolni takrorlang!',widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=['username','first_name','email']

    def clean_password2(self):
        data=self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Ikki parolingiz ham bir biriga teng bo\'lishi kerak')
        return data['password2']
    def send_email(self):
        send_review_email_task.delay(
         self.cleaned_data['username'],self.cleaned_data['first_name'],self.cleaned_data['email'],
            self.cleaned_data['username'],self.cleaned_data['password'],self.cleaned_data['password2']
        )


class UserEditForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email']
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['date_of_birth','photo']