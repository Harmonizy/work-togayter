from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Div
from ckeditor.widgets import CKEditorWidget
from django.forms import inlineformset_factory

from .models import Promotion, Quiz, Question, Choice

class PromotionForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(), label="")

    class Meta:
        model = Promotion
        fields = ['image', 'title', 'content', 'quiz', 'priority', 'type']
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
        self.helper.form_show_labels = True


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["text"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = True


QuestionFormSet = inlineformset_factory(
    Quiz,
    Question,
    form=QuestionForm,
    fields=["text"],
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
        self.helper.form_show_labels = True


ChoiceFormSet = inlineformset_factory(
    Question,
    Choice,
    form=ChoiceForm,
    fields=['text', 'is_correct'],
    extra=3,
    can_delete=True
)
