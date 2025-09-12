from django import forms
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column

from .models import HazardLog, CAP
from .choices import HazardSourceChoices
from safety.Report.models import BaseReport
from safety.Report.forms.fields import content_field

single_select_widget = forms.Select(attrs={'class': 'form-control js-example-basic-single'})

class HazardLogForm(forms.ModelForm):
    description = content_field(300, "รายละเอียดของอันตราย...")
    note = content_field(100, "หมายเหตุ...")

    class Meta:
        model = HazardLog
        exclude = ['code', 'serial_number']
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
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'เช่น อาคารซ่อมบำรุง โซน A'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial = kwargs.get('initial', {})
        if 'related_report_id' in initial:
            base_report = BaseReport.objects.get(id = initial['related_report_id'])
            self.fields['related_report'].initial = initial['related_report_id']
            self.fields['source'].initial = HazardSourceChoices.REPORT
            self.fields['title'].initial = base_report.title
            self.fields['description'].initial = base_report.content
            

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
                Column('title', css_class='form-group col-md-6 mb-0'),
                Column('location', css_class='form-group col-md-6 mb-0'),
            ),
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



class CAPForm(forms.ModelForm):
    description = content_field(300, "รายละเอียดการดำเนินการ...")
    class Meta:
        model = CAP
        fields = ['order', 'title', 'description', 'status', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'เช่น ดำเนินการอบรม'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('order', css_class='col-md-1'),
                Column('title', css_class='col-md-7'),
                Column('status', css_class='col-md-2'),
                Column('due_date', css_class='col-md-2'),
            ),
            Row(
                Column('description', css_class='col-md-12'),
            ),
        )


CAPFormSet = inlineformset_factory(
    parent_model=HazardLog,
    model=CAP,
    form=CAPForm,
    extra=1,
    can_delete=True
)
