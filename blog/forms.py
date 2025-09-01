from django import forms
from .models import NewsletterSubscriber, Category
from django_ckeditor_5.widgets import CKEditor5Widget
from django_ckeditor_5.fields import CKEditor5Field


class PostForm(forms.Form):
    title = forms.CharField(max_length=200)
    content = forms.CharField(widget=CKEditor5Widget())
    featured_image = forms.ImageField(required=False)
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    is_published = forms.BooleanField(required=False)

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your email address',
                'class': 'form-control'
            })
        }

