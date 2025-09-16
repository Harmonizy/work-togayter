from django import forms
from django.urls import reverse
from django.forms import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Div, Row, Column, Layout, Field, HTML
from crispy_forms.layout import Layout, Fieldset, Submit
from ckeditor.widgets import CKEditorWidget

from safety.Report.models import BaseReport, AviationReport, GroundReport
# , SafetyReport, ObservationReport
from .fields import  content_example, content_field, textarea_field, multi_select_widget, single_select_widget
from ..models import BaseReport, Image, Recommendation, File
from ..choices import ReportTypeChoices
from common.RTAFUser.models.RTAFUser import Affiliation


class BaseReportForm(forms.ModelForm):
    content = content_field(400, content_example)

    class Meta:
        model = BaseReport
        fields = [
            "report_type", "affiliation", "event_date", "event_time",
            "title", "content", "first_recommendation", "initial_action_taken",
            "anonymous", "comment"
        ]
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date', 'data-provider': 'flatpickr'}),
            'event_time': forms.TimeInput(attrs={'type': 'time'}),
            "anonymous": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "first_recommendation": textarea_field(),
            "initial_action_taken": textarea_field(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

        report_type = self.initial.get("report_type", "") 
        affiliation = self.initial.get("affiliation", None)
        
        if report_type:
            self.fields["report_type"].choices = [(choice.value, choice.label) for choice in ReportTypeChoices if choice.value == report_type]
        if affiliation:
            self.fields['affiliation'].queryset = self.fields['affiliation'].queryset.filter(id=affiliation)

        self.helper.layout = Layout(
            Row(
                Column('report_type', css_class='form-group col-6 col-md-3 mb-0'),
                Column('affiliation', css_class='form-group col-6 col-md-3 mb-0'),
                Column('event_date', css_class='form-group col-6 col-md-3 mb-0'),
                Column('event_time', css_class='form-group col-6 col-md-3 mb-0'),
            ),
            Div(
                Row(Column('title', css_class='form-group col-md-12 mb-0')),
                Row(Column(Field('content'), css_class='form-group col-md-12 mb-0')),
                css_id="title-content-part",
                css_class="my-wrapper-class",
            ),
            Row(
                Column('first_recommendation', css_class='form-group col-md-6 mb-0'),
                Column('initial_action_taken', css_class='form-group col-md-6 mb-0'),
            ),
            'comment',
            'anonymous',
        )


class GroundReportForm(forms.ModelForm):
    class Meta:
        model = GroundReport
        fields = [
            "category",
            "location",
        ]
        widgets = {            
            'category': single_select_widget,
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False  
        self.helper.layout = Layout(
            Row(
                Column('category', css_class='form-group col-md-3 mb-0'),
                Column('location', css_class='form-group col-md-9 mb-0'),
            ),
        )


class AviationReportForm(forms.ModelForm):
    class Meta:
        model = AviationReport
        fields = [
            'squadron',
            'aircraft',
            'system',
            'flight_phase',
        ]
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
            self.fields['aircraft'].queryset = self.fields['aircraft'].queryset.filter(affiliation=affiliation)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('squadron', css_class='form-group col-md-6 mb-0'),
                Column('aircraft', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('system', css_class='form-group col-md-6 mb-0'),
                Column('flight_phase', css_class='form-group col-md-6 mb-0'),
            ),
        )


# ========== Attachment Forms ==========
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["image", "comment"]


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["file", "comment"]


class RecommendationForm(forms.ModelForm):
    class Meta:
        model = Recommendation
        fields = ["note", "comment"]


# ========== Formsets ==========
ImageFormSet = inlineformset_factory(
    BaseReport, Image, form=ImageForm, extra=1, can_delete=False
)

FileFormSet = inlineformset_factory(
    BaseReport, File, form=FileForm, extra=1, can_delete=False
)

RecommendationFormSet = inlineformset_factory(
    BaseReport, Recommendation, form=RecommendationForm, extra=1, can_delete=False
)



# class HazardReportForm(forms.ModelForm):
#     class Meta:
#         model = HazardReport
#         fields = [
#             "first_recommendation",
#             "initial_action_taken",
#         ]
#         widgets = {
#             "first_recommendation": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
#             "initial_action_taken": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.helper = FormHelper()
#         self.helper.form_tag = False  # ให้ไป wrap form ใน template แทน
#         self.helper.layout = Layout(
#             Row(
#                 Column("first_recommendation", css_class="form-group col-md-6 mb-0"),
#                 Column("initial_action_taken", css_class="form-group col-md-6 mb-0"),
#             ),
#         )


# class SafetyReportForm(forms.ModelForm):
#     class Meta:
#         model = SafetyReport
#         fields = [  
#             'event', 
#             'damage_level', 
#             'injury_type', 
#             'location', 
#             'latitude', 
#             'longitude',
#         ]
#         widgets = {
#             'event': multi_select_widget,
#             'location': single_select_widget,
#         }        
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.helper = FormHelper()
#         self.helper.form_tag = False
#         self.helper.layout = Layout(
#         # HTML('<div class="tab-pane fade" id="description" role="tabpanel">'),
#             Row(
#                 Column('location', css_class='form-group col-md-4 mb-0'),
#                 Column('latitude', css_class='form-group col-md-2 mb-0'),
#                 Column('longitude', css_class='form-group col-md-2 mb-0'),
#                 Column('damage_level', css_class='form-group col-md-2 mb-0'),
#                 Column('injury_type', css_class='form-group col-md-2 mb-0'),
#             ),
#             'event',
#         # HTML('</div>')
#         )


# class ObsevationReportForm(forms.ModelForm):
#     class Meta:
#         model = ObservationReport
#         fields = [  
#             'behavior', 
#         ]
#         widgets = {
#             'behavior': single_select_widget,
#         }        
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.helper = FormHelper()
#         self.helper.form_tag = False
#         self.helper.layout = Layout(
#         # HTML('<div class="tab-pane fade" id="description" role="tabpanel">'),
#             Row(
#                 Column('behavior', css_class='form-group col-md-4 mb-0'),
#             ),
#         # HTML('</div>')
#         )


# #=====================================================

