# forms.py

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from django_select2.forms import ModelSelect2Widget

from .models import HazardLog
from safety.Report.forms.fields import content_field
from safety.Report.models import BaseReport
from common.RTAFUser.models import RTAFUser, Affiliation

class HazardLogForm(forms.ModelForm):
    description = content_field(300, "รายละเอียดของอันตราย...")
    note = content_field(100, "หมายเหตุ...")
    class Meta:
        model = HazardLog
        fields = '__all__'
        widgets = {
            # 'assign_to': ModelSelect2Widget(
            #     model=RTAFUser,
            #     search_fields=['first_name__icontains', ],
            #     attrs={'class': 'django-select2 form-control',},
            # ),
            # 'affiliation': ModelSelect2Widget(
            #     model=Affiliation,
            #     search_fields=['name__icontains', ],
            #     attrs={'class': 'django-select2 form-control',},
            # ),
            # 'related_report': ModelSelect2Widget(
            #     model=BaseReport,
            #     search_fields=['title__icontains', ],
            #     attrs={'class': 'django-select2 form-control',},
            # ),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Crispy Forms Helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False  # Form tag will be in the template

        self.helper.layout = Layout(
            Row(
                Column('category', css_class='form-group col-md-3 mb-0'),
                Column('affiliation', css_class='form-group col-md-3 mb-0'),
                Column('assign_to', css_class='form-group col-md-3 mb-0'),
                Column('date', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('location', css_class='form-group col-md-12 mb-0'),
            ),
            'description',
            Row(
                Column('inspect', css_class='form-group col-md-2 mb-0'),
                Column('initial_likelihood', css_class='form-group col-md-2 mb-0'),
                Column('initial_severity', css_class='form-group col-md-2 mb-0'),\
                Column('source', css_class='form-group col-md-2 mb-0'),
                Column('related_report', css_class='form-group col-md-2 mb-0'),
            ),
            'note',
        )
