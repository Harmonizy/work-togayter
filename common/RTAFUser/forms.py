from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field
from crispy_forms.bootstrap import FormActions

from .models import RTAFUser, Affiliation

class MyAuthForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))    


class RTAFUserForm(forms.ModelForm):
    class Meta:
        model = RTAFUser
        fields = [
            'username', 'rank', 'first_name', 'last_name','position', 'email', 
            'af_id', 'person_id',
            'affiliation', 'work_affiliation'
        ]
        labels = {
            'first_name': _('ชื่อ'),
            'last_name': _('นามสกุล'),
            'person_id': _('เลขประจำตัวประชาชน (13 หลัก)'),
            'af_id': _('เลขประจำตัว ขรก. (10 หลัก)'),
            'email': _('อีเมล์'),
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'readonly': 'true'}),            
            'person_id': forms.TextInput(attrs={'required': 'true'}),
            'af_id': forms.TextInput(attrs={'required': 'true'}),
            'rank': forms.Select(),            
            'affiliation': forms.Select(),
            'work_affiliation': forms.Select(),
        }
    
    def __init__(self, *args, **kwargs):
        super(RTAFUserForm, self).__init__(*args, **kwargs)
        self.fields['person_id'].widget.attrs['readonly'] =  bool(kwargs['instance'].person_id)
        self.fields['af_id'].widget.attrs['readonly'] =  bool(kwargs['instance'].af_id)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-2'),
                Column('rank', css_class='form-group col-md-2'),
                Column('first_name', css_class='form-group col-md-3'),
                Column('last_name', css_class='form-group col-md-3'),
                Column('email', css_class='form-group col-md-2'),
                css_class='form-row'
            ),
            Row(
                Column('af_id', css_class='form-group col-md-2'),
                Column('person_id', css_class='form-group col-md-2'),
                Column('position', css_class='form-group col-md-4'),
                Column('affiliation', css_class='form-group col-md-2'),
                Column('work_affiliation', css_class='form-group col-md-2'),
                css_class='form-row'
            )
        )
                       

class AffiliationForm(forms.ModelForm):
    class Meta:
        model = Affiliation
        fields = ['hris_code', 'short_name', 'full_name', 'is_rtaf_directed', 'super_affiliation']
        
    def __init__(self, *args, **kwargs):
        super(AffiliationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('hris_code', css_class='form-group col-md-2'),
                Column('short_name', css_class='form-group col-md-2'),
                Column('full_name', css_class='form-group col-md-4'),
                Column('is_rtaf_directed', css_class='form-group col-md-2'),
                Column('super_affiliation', css_class='form-group col-md-2'),
                css_class='form-row'
            ),
            FormActions(
                Submit('submit', 'บันทึกข้อมูล')
            )
        )

