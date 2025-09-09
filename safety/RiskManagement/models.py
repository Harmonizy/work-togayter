from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from safety.Data.models import Event
from common.RTAFUser.models.RTAFUser import RTAFUser, Affiliation
from .choices import HazardLogStatusChoices, InspectChoices, CAPStatusChoices

class HazardCategory(models.Model):
    event = models.ForeignKey(Event, verbose_name="ชื่อเหตุการณ์", on_delete=models.CASCADE, related_name="hazard_categories")
    description = models.TextField("รายละเอียด")

    class Meta:
        verbose_name = verbose_name_plural = "1. หมวดหมู่ความเสี่ยง"

    def __str__(self):
        return self.event.name


class HazardLog(models.Model):
    category = models.ForeignKey(HazardCategory, verbose_name="หมวดหมู่", on_delete=models.CASCADE, related_name="hazard_logs")
    code = models.CharField("รหัส", max_length=8, unique=True)
    description = models.TextField("รายละเอียด", null=False, blank=False)
    affiliation = models.ForeignKey(Affiliation, verbose_name="หน่วยงาน", on_delete=models.CASCADE, related_name="hazard_logs")
    assign_to = models.ForeignKey(RTAFUser, verbose_name="ผู้รับผิดชอบ", on_delete=models.SET_NULL, null=True, blank=True)

    date = models.DateField("วันที่เกิดเหตุ", null=True, blank=True)
    location = models.CharField("สถานที่เกิดเหตุ", max_length=255, null=True, blank=True)

    status = models.CharField("สถานะ", max_length=1, choices=HazardLogStatusChoices.choices, default=HazardLogStatusChoices.OPEN, null=True, blank=True)
    inspect = models.CharField("การสอบสวน", max_length=1, choices=InspectChoices.choices, default=InspectChoices.START_INVESTIGATION, null=True, blank=True)

    initial_likelihood = models.PositiveSmallIntegerField("โอกาสเริ่มต้น", validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    initial_severity = models.PositiveSmallIntegerField("ความรุนแรงเริ่มต้น", validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    initial_risk_level = models.PositiveSmallIntegerField("ระดับความเสี่ยงเริ่มต้น", validators=[MinValueValidator(1), MaxValueValidator(25)], null=True, blank=True)

    residual_likelihood = models.PositiveSmallIntegerField("โอกาสหลังแก้ไข", validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    residual_severity = models.PositiveSmallIntegerField("ความรุนแรงหลังแก้ไข", validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    residual_risk_level = models.PositiveSmallIntegerField("ระดับความเสี่ยงหลังแก้ไข", validators=[MinValueValidator(1), MaxValueValidator(25)], null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = verbose_name_plural = "2. ทะเบียนความเสี่ยง"

    def __str__(self):
        return f"{self.code} - {self.category.event.name}"
    
    def save(self, *args, **kwargs):
        self.initial_risk_level = (self.initial_likelihood or 0) * (self.initial_severity or 0)
        self.residual_risk_level = (self.residual_likelihood or 0) * (self.residual_severity or 0)
        super().save(*args, **kwargs)


class CAP(models.Model):

    hazard_log = models.ForeignKey(HazardLog, verbose_name="Hazard Log", on_delete=models.CASCADE, related_name="caps")
    title = models.CharField("หัวข้อ", max_length=255)
    description = models.TextField("รายละเอียด", null=True, blank=True)

    status = models.CharField("สถานะ", max_length=2, choices=CAPStatusChoices.choices, default=CAPStatusChoices.PLANNING, null=True, blank=True)

    due_date = models.DateField("วันครบกำหนด", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = verbose_name_plural = "3. CAP"

    def __str__(self):
        return f"{self.title} ({self.status})"