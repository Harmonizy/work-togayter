from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Div
from ckeditor.widgets import CKEditorWidget

from .models import Promotion

class PromotionForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(), label="")

    class Meta:
        model = Promotion
        fields = ['image', 'title', 'content', 'quiz']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'หัวข้อประกาศ'}),
            'quiz': forms.Select(attrs={'class': 'form-select'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].required = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(

            Row(
                Column('image', css_class='form-group col-md-6 mb-0'),
                Column('title', css_class='form-group col-md-6 mb-0'),
            ),

            # ✅ content ไม่มีหัวข้อ (label="")
            Div(
                Row(
                    Column(Field('content', css_class='mb-3'), css_class='form-group col-md-12 mb-0'),
                ),
                css_id="title-content-part",
                css_class="my-wrapper-class",
            ),

            Row(
                Column('quiz', css_class='form-group col-md-4 mb-0'),
            ),
        )
