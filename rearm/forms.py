# forms.py
from django import forms
from .models import DemoBooking

class DemoBookingForm(forms.ModelForm):
    class Meta:
        model = DemoBooking
        fields = ['name', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
        }