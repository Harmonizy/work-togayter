from django import forms
from django.forms import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Row, Column, Layout, Field, HTML
from crispy_forms.layout import Layout, Fieldset, Submit
from ckeditor.widgets import CKEditorWidget

from safety.Report.models import BaseReport
# , AviationReport, GroundReport, SafetyReport, ObservationReport
from ..models import BaseReport, Image, Recommendation, File


# ========== Base Forms ==========
single_select_widget = forms.Select(
    attrs={
        'class': 'js-example-basic-single'
    }
)

multi_select_widget = forms.SelectMultiple(
    attrs={
        'class': 'js-example-basic-multiple',
        'multiple': 'multiple'
    }
)

content_example = """
            <h3><strong>รายละเอียดเหตุการณ์</strong></h3>
            <p>
                ระหว่างการบินในภารกิจฝึกประจำวัน นักบินตรวจพบสัญญาณผิดปกติของระบบไฮดรอลิกเบอร์ 2 ขณะอยู่ในระดับความสูงประมาณ 3,000 ฟุต 
                จึงดำเนินการตามขั้นตอนการแก้ไขเหตุฉุกเฉินตามคู่มือ และนำอากาศยานลงจอดที่สนามบินอย่างปลอดภัย
            </p>

            <h3><strong>การตอบสนองเบื้องต้น</strong></h3>
            <p>
                เจ้าหน้าที่ภาคพื้นดำเนินการตรวจสอบระบบทันทีหลังเครื่องลงจอด และไม่อนุญาตให้ใช้งานอากาศยานลำนั้นต่อจนกว่าจะผ่านการตรวจสอบระบบโดยละเอียด
            </p>

            <h3><strong>สาเหตุที่เป็นไปได้</strong></h3>
            <ul>
                <li>ความเสื่อมสภาพของวาล์วควบคุมภายในระบบไฮดรอลิก</li>
                <li>แรงดันไฮดรอลิกต่ำกว่าค่ามาตรฐานที่กำหนด</li>
            </ul>
        """

recommendation_example = """
            <h3><strong>คำแนะนำเบื้องต้น</strong></h3>
            <p>
                ควรตรวจสอบระบบไฮดรอลิกอย่างละเอียด และดำเนินการซ่อมแซมตามความจำเป็น
            </p>
        """

initial_action_taken_example = """
            <h3><strong>การดำเนินการเบื้องต้น</strong></h3>
            <p>
                เจ้าหน้าที่ภาคพื้นดำเนินการตรวจสอบระบบทันทีหลังเครื่องลงจอด และไม่อนุญาตให้ใช้งานอากาศยานลำนั้นต่อจนกว่าจะผ่านการตรวจสอบระบบโดยละเอียด
            </p>
"""

content_field = lambda height, example : forms.CharField(
    widget=CKEditorWidget(
        attrs={
            'class': 'ckeditor-classic',
            'style': f'max-height: {height}px;',
        }
    ),
    label="",
    initial=example
)

textarea_field = lambda rows=3, cols=40: forms.Textarea(attrs={"cols": cols, "rows": rows})
   