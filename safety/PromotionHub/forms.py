from django import forms
from .models import Promotion

class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ['image', 'title', 'content', 'status', 'publish', 'quiz']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }
