from django import forms
from django.forms import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, Field, HTML
from ckeditor.widgets import CKEditorWidget

from .fields import content_example, content_field, textarea_field, multi_select_widget, single_select_widget
from ..models import (
    BaseReport, Image, Recommendation, File, AviationReport, GroundReport,
    Participant, ReferenceReport
)
from ..choices import ReportTypeChoices, ExampleContentChoices
from common.RTAFUser.models.RTAFUser import Affiliation


class BaseInlineFormSet(forms.BaseInlineFormSet):
    """This enables CrispyForms to respect each subform's layout."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True


class BaseReportForm(forms.ModelForm):
    content = content_field(400, content_example)
    
    example_content = forms.ChoiceField(
        choices=ReportTypeChoices.choices,
        required=False,
        label="ตัวอย่างเนื้อหารายงาน",
        widget=forms.Select(attrs={
            "class": "form-select",
            "id": "example-content-select"
        })
    )

    class Meta:
        model = BaseReport
        fields = [
            "report_type", "affiliation", "location_affiliation", "event_date", "event_time",
            "title", "content", "first_recommendation", "initial_action_taken",
            "anonymous", "comment"
        ]
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date', 'data-provider': 'flatpickr'}),
            "anonymous": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "first_recommendation": textarea_field(),
            "initial_action_taken": textarea_field(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['event_time'] = forms.TimeField(
            input_formats=['%H:%M'],
            widget=forms.TimeInput(
                format='%H:%M',
                attrs={'type': 'time'}
            )
        )
        self.fields['event_time'].label = "เวลาเกิดเหตุ"

        report_type = self.initial.get("report_type", "")
        affiliation = self.initial.get("affiliation", None)

        if report_type:
            self.fields["report_type"].choices = [
                (choice.value, choice.label) for choice in ReportTypeChoices if choice.value == report_type
            ]

        if affiliation:
            if isinstance(affiliation, int):
                affiliation = Affiliation.objects.get(id=affiliation)
            self.fields['affiliation'].queryset = Affiliation.objects.filter(id=affiliation.id)

        # Crispy Layout
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('report_type', css_class='col-md-4'),
                Column('affiliation', css_class='col-md-2'),
                Column('location_affiliation', css_class='col-md-2'),
                Column('event_date', css_class='col-md-2'),
                Column('event_time', css_class='col-md-2'),
            ),
            Div(
                Row(
                    Column('title', css_class='col-md-9'),
                    Column('example_content', css_class='col-md-2'),
                    Column(
                        HTML("""
                            <a id="example-download-btn"
                            class="btn btn-outline-primary mt-4 d-none"
                            target="_blank">
                            ดาวน์โหลดตัวอย่าง
                            </a>
                        """),
                        css_class="col-md-1"
                    ),
                    ),
                
                Row(Column(Field('content'), css_class='col-md-12')),
                css_id="title-content-part",
            ),
            Row(
                Column('first_recommendation', css_class='col-md-6'),
                Column('initial_action_taken', css_class='col-md-6'),
            ),
            'comment',
            'anonymous'
        )
    


class GroundReportForm(forms.ModelForm):
    class Meta:
        model = GroundReport
        fields = ["accident_type", "category", "location"]
        widgets = {'category': single_select_widget}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('accident_type', css_class='col-md-4'),
                Column('category', css_class='col-md-4'),
                Column('location', css_class='col-md-4'),
            )
        )


class AviationReportForm(forms.ModelForm):
    class Meta:
        model = AviationReport
        fields = ['squadron', 'aircraft', 'system', 'flight_phase', 'plane_number', 'air_control']
        widgets = {
            'squadron': single_select_widget,
            'aircraft': single_select_widget,
            'system': multi_select_widget,
            'flight_phase': multi_select_widget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        affiliation = self.initial.get("affiliation", None)
        if affiliation:
            self.fields['squadron'].queryset = self.fields['squadron'].queryset.filter(affiliation=affiliation)
            self.fields['aircraft'].queryset = self.fields['aircraft'].queryset.filter(squadron__affiliation=affiliation)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('squadron', css_class='col-4 col-md-4'),
                Column('plane_number', css_class='col-4 col-md-4'),
                Column('air_control', css_class='col-4 col-md-4'),
            ),
            Row(
                Column('aircraft', css_class='col-4 col-md-4'),
                Column('system', css_class='col-4 col-md-4'),
                Column('flight_phase', css_class='col-4 col-md-4'),
            )
        )


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ["full_name", "role", "injury_level", "note"]
        widgets = {
            'role': single_select_widget,
            'injury_level': single_select_widget,
            'note': forms.TextInput(attrs={'placeholder': 'หมายเหตุเพิ่มเติม...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('full_name', css_class='col-3 col-md-3'),
                Column('role', css_class='col-3 col-md-3'),
                Column('injury_level', css_class='col-3 col-md-3'),
                Column('note', css_class='col-3 col-md-3'),
            )
        )


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'comment']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'comment': forms.TextInput(attrs={'placeholder': 'หมายเหตุเพิ่มเติม...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['comment'].label = ''

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('image', css_class='col-8 col-md-8'),
                Column('comment', css_class='col-4 col-md-4'),
            )
        )


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file', 'comment']
        widgets = {
            'file': forms.ClearableFileInput(attrs={
                'accept': (
                    'application/pdf,'
                    'application/msword,'
                    'application/vnd.ms-excel,'
                    'application/vnd.ms-powerpoint,'
                    'application/vnd.openxmlformats-officedocument.wordprocessingml.document,'
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,'
                    'application/vnd.openxmlformats-officedocument.presentationml.presentation'
                )
            }),
            'comment': forms.TextInput(attrs={'placeholder': 'หมายเหตุเพิ่มเติม...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].required = False
        self.fields['comment'].label = ''

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('file', css_class='col-8 col-md-8'),
                Column('comment', css_class='col-4 col-md-4'),
            )
        )


class RecommendationForm(forms.ModelForm):
    class Meta:
        model = Recommendation
        fields = ['note', 'comment']
        widgets = {
            'note': textarea_field(2),
            'comment': forms.TextInput(attrs={'placeholder': 'หมายเหตุเพิ่มเติม...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['note'].required = False
        self.fields['comment'].label = ''

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('note', css_class='col-8 col-md-8'),
                Column('comment', css_class='col-4 col-md-4'),
            )
        )


class ReferenceReportForm(forms.ModelForm):
    class Meta:
        model = ReferenceReport
        fields = ["report", "note"]
        widgets = {
            'report': single_select_widget,
            'note': forms.Textarea(attrs={'placeholder': 'หมายเหตุเพิ่มเติม...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('report', css_class='col-6 col-md-6'),
                Column('note', css_class='col-6 col-md-6'),
            )
        )



ParticipantFormSet = inlineformset_factory(
    BaseReport, Participant,
    form=ParticipantForm,
    formset=BaseInlineFormSet,
    fk_name='base_report',
    extra=1,
    can_delete=True
)

ImageFormSet = inlineformset_factory(
    BaseReport, Image,
    form=ImageForm,
    formset=BaseInlineFormSet,
    fk_name='base_report',
    extra=1,
    can_delete=True
)

FileFormSet = inlineformset_factory(
    BaseReport, File,
    form=FileForm,
    formset=BaseInlineFormSet,
    fk_name='base_report',
    extra=1,
    can_delete=True
)

RecommendationFormSet = inlineformset_factory(
    BaseReport, Recommendation,
    form=RecommendationForm,
    formset=BaseInlineFormSet,
    fk_name='base_report',
    extra=1,
    can_delete=True
)

ReferenceReportFormSet = inlineformset_factory(
    BaseReport, ReferenceReport,
    form=ReferenceReportForm,
    formset=BaseInlineFormSet,
    fk_name="base_report",
    extra=1,
    can_delete=True
)



