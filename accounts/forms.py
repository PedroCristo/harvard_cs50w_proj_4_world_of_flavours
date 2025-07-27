from django import forms
# from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, UserProfile


class CustomRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            self.add_error('password_confirm', 'Passwords do not match')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user    
    

class CustomLoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput())
    password = forms.CharField(required=True, widget=forms.PasswordInput())    


class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ['user_name', 'location', 'user_image', 'user_social_media', 'bio']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email