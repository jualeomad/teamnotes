from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'team')

class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30, label="Username or Email")

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            user = CustomUser.objects.filter(email=username).first()

            if user is None:
                user = CustomUser.objects.filter(username=username).first()

            if user is None or not user.check_password(password):
                raise forms.ValidationError(
                    "Invalid username or password. Please try again."
                )
            self.user_cache = user

        return self.cleaned_data
