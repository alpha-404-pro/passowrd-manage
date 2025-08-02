from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import PasswordEntry

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

class PasswordEntryForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        }),
        required=True
    )

    class Meta:
        model = PasswordEntry
        fields = ['website_name', 'username']
        widgets = {
            'website_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Website Name'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username/Email (Optional)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make username field optional
        self.fields['username'].required = False

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.user = user
        
        # Get the password from cleaned_data
        password = self.cleaned_data.get('password')
        if password:
            instance.set_password(password)
        
        if commit:
            instance.save()
        return instance
