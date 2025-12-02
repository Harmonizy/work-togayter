from datetime import date

from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import reverse

from ckeditor.fields import RichTextField

from ..choices import QuestionCategoryChoices, AnswerChoices
from safety.Data.models import Event, Aircraft, AircraftSystem, FlightPhase, Location, GroundSafetyCategory, Keyword, Role
from common.RTAFUser.models import RTAFUser, Affiliation, Squadron
from safety.Report.models import BaseReport


class Question(models.Model):
    category = models.IntegerField(verbose_name="หมวดหมู่", choices=QuestionCategoryChoices.choices, null=True, blank=True)
    code = models.CharField(verbose_name="รหัส", max_length=8, unique=True)
    definition = models.CharField(verbose_name="นิยาม",max_length=255)
    description = models.TextField(verbose_name="ข้อพิจารณาทางทหาร/การปรับใช้", blank=True, null=True)
    note = models.TextField(verbose_name="การอ้างอิงมาตรฐาน", blank=True, null=True)


    def __str__(self):
        return f"{self.code} - {self.definition}"
    
    class Meta:
        verbose_name = verbose_name_plural = "2.1 คําถาม"


class SixA(models.Model):
    report = models.ForeignKey(BaseReport, verbose_name="รายงาน", on_delete=models.CASCADE)
    user = models.ForeignKey(RTAFUser, verbose_name="ผู้บันทึก", on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(verbose_name="วันที่สร้าง", auto_now_add=True)

    def __str__(self):
        return f"6A โดย {self.user} ของรายงาน {self.report}"

    class Meta:
        verbose_name = verbose_name_plural = "2. 6A"


class Answer(models.Model):
    sixA = models.ForeignKey(SixA, verbose_name="6A", on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, verbose_name="คําถาม", on_delete=models.CASCADE)

    answer = models.BooleanField(verbose_name="คําตอบ")
    note = models.TextField(verbose_name="หมายเหตุ", blank=True, null=True)

    class Meta:
        unique_together = ("sixA", "question")

    def __str__(self):
        return f"{self.question.code} = {self.answer}"