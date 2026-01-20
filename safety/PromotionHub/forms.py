from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Div, Submit
from django.forms import inlineformset_factory
from django.forms import ClearableFileInput

from ckeditor.widgets import CKEditorWidget

from .models import Promotion, Quiz, Question, Choice, Document, DocumentFile


class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["multiple"] = True
        super().__init__(*args, **kwargs)
        

class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ['title', 'content', 'quiz']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'หัวข้อประกาศ'
            }),
            'quiz': forms.Select(attrs={'class': 'form-select'}),
            'content': CKEditorWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['content'].required = False

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-6 mb-0'),
            ),
            Div(
                Field('content', css_class='mb-3'),
                css_id="title-content-part",
            ),
            Row(
                Column('quiz', css_class='form-group col-md-4 mb-0'),
            ),
        )


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["title", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["text"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


QuestionFormSet = inlineformset_factory(
    Quiz,
    Question,
    form=QuestionForm,
    extra=1,
    can_delete=True
)


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ["text", "is_correct"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


ChoiceFormSet = inlineformset_factory(
    Question,
    Choice,
    form=ChoiceForm,
    extra=1,
    can_delete=True
)


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["title", "description", "promotion"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"

        self.helper.layout = Layout(
            Row(
                Column("title", css_class="col-md-6"),
                Column("promotion", css_class="col-md-6"),
            ),
            "description",

            # ⭐ ปุ่มบันทึกที่คุณลบออกไป ต้องใส่กลับมา ⭐
            Submit("submit", "บันทึก", css_class="btn btn-primary mt-3")
        )


class DocumentFileForm(forms.Form):
    files = forms.FileField(
        required=False,
        widget=MultipleFileInput(attrs={
            "class": "form-control"
        })
    )


