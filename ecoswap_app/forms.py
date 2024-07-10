

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Item, Exchange

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


class ExchangeForm(forms.ModelForm):
    class Meta:
        model = Exchange
        fields = ['offered_item']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ExchangeForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['offered_item'].queryset = Item.objects.filter(user=user)
