

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Item

class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'address', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'item_description', 'item_category', 'item_condition', 'item_value']
        widgets = {
            'item_description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
