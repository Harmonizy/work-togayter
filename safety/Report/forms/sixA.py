from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Row, Column

from safety.Report.models.sixA import SixA, Answer, Question
from common.RTAFUser.models import RTAFUser


class AnswerInlineFormSet(forms.BaseInlineFormSet):
    """Enable CrispyForms layout for each inline form."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True


class SixAForm(forms.ModelForm):
    class Meta:
        model = SixA
        fields = ["report", "user"]

        widgets = {
            "report": forms.HiddenInput(), 
            "user": forms.HiddenInput(), 
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        # ตั้งค่าผู้บันทึกอัตโนมัติ ถ้ายังไม่มีค่า
        if not self.instance.pk and self.request:
            self.fields["user"].initial = self.request.user

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'report',
            'user'
        )


class AnswerForm(forms.ModelForm):
    answer = forms.BooleanField(
        required=False, 
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="คำตอบ"
    )

    class Meta:
        model = Answer
        fields = ["question", "answer", "note"]
        widgets = {
            "question": forms.HiddenInput(),
            "note": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 1,
                "placeholder": "หมายเหตุ (ถ้ามี)..."
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
