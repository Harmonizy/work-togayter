from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Row, Column

from .fields import content_example, content_field, textarea_field, multi_select_widget
from ..models import BaseReport, Image, Recommendation, File


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True
    

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]
        return [single_file_clean(data, initial)]



# -------------------------------------------------------
# 1) BaseInlineFormSet (หัวใจสำคัญ)
# -------------------------------------------------------
class BaseInlineFormSet(forms.BaseInlineFormSet):
    """Enable crispy layout inside inline formset"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True


# -------------------------------------------------------
# 2) Image Form
# -------------------------------------------------------
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
                Column('image', css_class='col-md-8'),
                Column('comment', css_class='col-md-4'),
            )
        )


# -------------------------------------------------------
# 3) Recommendation Form
# -------------------------------------------------------
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
                Column('note', css_class='col-md-8'),
                Column('comment', css_class='col-md-4'),
            )
        )


# -------------------------------------------------------
# 4) File Form
# -------------------------------------------------------
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
                Column('file', css_class='col-md-8'),
                Column('comment', css_class='col-md-4'),
            )
        )


class BulkAttachmentForm(forms.Form):
    bulk_images = MultipleFileField(
        required=False,
        label="เพิ่มรูปภาพ (แต่ละภาพต้องไม่เกิน 3MB)"
    )

    bulk_files = MultipleFileField(
        required=False,
        label="เพิ่มไฟล์ (แต่ละไฟล์ต้องไม่เกิน 10MB)"
    )

    def save(self, base_report, user):
        from ..models import Image, File
        from django.core.exceptions import ValidationError

        for img in self.cleaned_data.get("bulk_images", []):
            if not img.content_type.startswith("image/"):
                continue   # หรือ raise ValidationError
            Image.objects.create(
                base_report=base_report,
                image=img,
                recorder=user
            )

        for f in self.cleaned_data.get("bulk_files", []):
            if f.content_type.startswith("image/"):
                continue
            File.objects.create(
                base_report=base_report,
                file=f,
                recorder=user
            )




# -------------------------------------------------------
# 5) Formsets — ใช้ BaseInlineFormSet ให้ครบ
# -------------------------------------------------------
ImageFormSet = forms.inlineformset_factory(
    BaseReport, Image,
    form=ImageForm,
    formset=BaseInlineFormSet,
    extra=1,
    can_delete=True
)

RecommendationFormSet = forms.inlineformset_factory(
    BaseReport, Recommendation,
    form=RecommendationForm,
    formset=BaseInlineFormSet,
    extra=1,
    can_delete=True
)

FileFormSet = forms.inlineformset_factory(
    BaseReport, File,
    form=FileForm,
    formset=BaseInlineFormSet,
    extra=1,
    can_delete=True
)
