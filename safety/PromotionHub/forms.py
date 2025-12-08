from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Div, Submit
from django.forms import inlineformset_factory

from tinymce.widgets import TinyMCE
from ckeditor.widgets import CKEditorWidget

from .models import Promotion, Quiz, Question, Choice, Document, DocumentFile

class PromotionForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Promotion
        fields = ['image', 'title', 'content', 'priority', 'type', 'quiz']
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

            Div(
                Row(
                    Column(Field('content', css_class='mb-3'), css_class='form-group col-md-12 mb-0'),
                ),
                css_id="title-content-part",
                css_class="my-wrapper-class",
            ),

            Row(
                Column('priority', css_class='form-group col-md-4 mb-0'),
                Column('type', css_class='form-group col-md-4 mb-0'),
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


class DocumentFileForm(forms.ModelForm):
    class Meta:
        model = DocumentFile
        fields = ["file", "title", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False 
        self.helper.layout = Layout(
            "file",
            "title",
            "description",
        )

        