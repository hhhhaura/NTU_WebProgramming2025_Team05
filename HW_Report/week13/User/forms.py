from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    
    class Meta:
        model = Profile
        fields = ('bio', 'birth_date', 'phone_number', 'preferred_payment_method')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'preferred_payment_method': forms.Select(choices=[
                ('', 'Select payment method'),
                ('bank_transfer', 'Bank Transfer'),
                ('line_pay', 'Line Pay'),
                ('cash', 'Cash'),
            ])
        } 