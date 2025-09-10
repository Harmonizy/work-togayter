from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column

from .models import HazardLog
from safety.Report.forms.fields import content_field
from safety.Report.models import BaseReport
from common.RTAFUser.models import RTAFUser, Affiliation

single_select_widget = forms.Select(attrs={'class': 'form-control js-example-basic-single'})


class HazardLogForm(forms.ModelForm):
    description = content_field(300, "รายละเอียดของอันตราย...")
    note = content_field(100, "หมายเหตุ...")

    class Meta:
        model = HazardLog
        fields = '__all__'
        widgets = {
            'category': single_select_widget,
            'affiliation': single_select_widget,
            'assign_to': single_select_widget,
            'related_report': single_select_widget,
            'status': single_select_widget,
            'inspect': single_select_widget,
            'initial_likelihood': single_select_widget,
            'initial_severity': single_select_widget,
            'residual_likelihood': single_select_widget,
            'residual_severity': single_select_widget,
            'source': single_select_widget,
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'เช่น RISK0001'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Column('category', css_class='form-group col-md-3 mb-0'),
                Column('affiliation', css_class='form-group col-md-3 mb-0'),
                Column('assign_to', css_class='form-group col-md-3 mb-0'),
                Column('date', css_class='form-group col-md-3 mb-0'),
            ),
            
            Row(
                Column('code', css_class='form-group col-md-3 mb-0'),
                Column('location', css_class='form-group col-md-12 mb-0')),
            'description',
            Row(
                Column('inspect', css_class='form-group col-md-2 mb-0'),
                Column('initial_likelihood', css_class='form-group col-md-2 mb-0'),
                Column('initial_severity', css_class='form-group col-md-2 mb-0'),
                Column('source', css_class='form-group col-md-2 mb-0'),
                Column('related_report', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('status', css_class='form-group col-md-2 mb-0'),
                Column('residual_likelihood', css_class='form-group col-md-2 mb-0'),
                Column('residual_severity', css_class='form-group col-md-2 mb-0'),
            ),
            'note',
        )
