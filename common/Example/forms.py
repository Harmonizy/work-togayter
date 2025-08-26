from django import forms
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column

class FeedbackForm(forms.Form):
    name = forms.CharField(label="ชื่อ", max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'John Doe',
            'class': 'form-control',
        })
    )
    
    email = forms.EmailField(label="Email", 
        widget=forms.EmailInput(attrs={
            'placeholder': 'user@example.com',
            'class': 'form-control',
        })
    )
    
    message = forms.CharField(label="ข้อความ", 
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter your feedback here...',
            'class': 'form-control',
            'rows': 4,
        })
    )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if "example" not in  email:
            raise ValidationError("เฉพาะ email example เท่านั้น")
        return email
    
    def clean_message(self):
        message = self.cleaned_data['message']
        if len(message) < 10:
            raise ValidationError("ข้อความต้องยาวกว่า  10 ตัวอักษร")
        return message
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # use crispy form helper
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6'),
                Column('email', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('message', css_class='form-group col-md-12'),
                css_class='form-row'
            ),
        )
        