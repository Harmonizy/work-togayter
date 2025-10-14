from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Row, Column

from .fields import    content_example, content_field, textarea_field, multi_select_widget
from ..models import BaseReport, Image, Recommendation, File


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'comment']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'accept': 'image/*',
            }),            
            'comment': forms.TextInput(attrs={
                'placeholder': 'หมายเหตุเพิ่มเติม...',
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].label = ''
        self.fields['comment'].label = ''
                
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('image', css_class='form-group col-md-8 mb-0'),
                Column('comment', css_class='form-group col-md-4 mb-0'),
            )
        )
        

class RecommendationForm(forms.ModelForm):
    class Meta:
        model = Recommendation
        fields = ['note', 'comment']
        widgets = {
            'note': textarea_field(2),
            'comment': forms.TextInput(attrs={
                'placeholder': 'หมายเหตุเพิ่มเติม...',
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['note'].label = ''
        self.fields['comment'].label = ''
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('note', css_class='form-group col-md-8 mb-0'),
                Column('comment', css_class='form-group col-md-4 mb-0'),
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
                ),
            }),            
            'comment': forms.TextInput(attrs={
                'placeholder': 'หมายเหตุเพิ่มเติม...',
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['file'].label = ''
        self.fields['comment'].label = ''
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('file', css_class='form-group col-md-8 mb-0'),
                Column('comment', css_class='form-group col-md-4 mb-0'),
            )
        )


ImageFormSet = forms.inlineformset_factory(
    BaseReport, Image,
    form = ImageForm,
    extra=1, can_delete=True
)


RecommendationFormSet = forms.inlineformset_factory(
    BaseReport, Recommendation,
    form = RecommendationForm,
    extra=1, can_delete=True
)


FileFormSet = forms.inlineformset_factory(
    BaseReport, File,
    form = FileForm,
    extra=1, can_delete=True
)
