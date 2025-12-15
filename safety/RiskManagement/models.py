from django.db import models
from django.db.models import Max
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

from safety.Data.models import Event
from common.RTAFUser.models.RTAFUser import RTAFUser, Affiliation
from .choices import HazardLogStatusChoices, HazardSourceChoices, InspectChoices, CAPStatusChoices, LikelihoodChoices, SeverityChoices


class HazardCategory(models.Model):
    event = models.ForeignKey(Event, verbose_name="ชื่อเหตุการณ์", on_delete=models.CASCADE, related_name="hazard_categories")
    description = models.TextField(verbose_name="รายละเอียด")

    class Meta:
        verbose_name = verbose_name_plural = "2. หมวดหมู่ความเสี่ยง"

    def __str__(self):
        return self.event.name


class HazardSource(models.Model):
    name = models.CharField(verbose_name="ชื่อ", max_length=100)
    description = models.CharField(verbose_name="รายละเอียด", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = "4. แหล่งที่มา"

    def __str__(self):
        return self.name


class HazardLog(models.Model):
    category = models.ForeignKey(HazardCategory, verbose_name="หมวดหมู่", on_delete=models.CASCADE, related_name="hazard_logs")
    code = models.CharField(verbose_name="รหัส", max_length=8, unique=True, null=True, blank=True)
    serial_number = models.PositiveIntegerField(verbose_name="ลำดับที่", default=1, null=True, blank=True)
    title = models.CharField(verbose_name="หัวข้อ", max_length=255, null=False, blank=False)
    description = models.TextField(verbose_name="รายละเอียด", null=False, blank=False)
    affiliation = models.ForeignKey(Affiliation, verbose_name="หน่วยงาน", on_delete=models.CASCADE, related_name="hazard_logs")
    assign_to = models.ForeignKey(RTAFUser, verbose_name="ผู้รับผิดชอบ", on_delete=models.SET_NULL, null=True, blank=True)

    date = models.DateField(verbose_name="วันที่เกิดเหตุ", null=True, blank=True)
    location = models.CharField(verbose_name="สถานที่เกิดเหตุ", max_length=255, null=True, blank=True)

    status = models.CharField(verbose_name="สถานะ", max_length=1, choices=HazardLogStatusChoices.choices, default=HazardLogStatusChoices.OPEN, null=True, blank=True)
    inspect = models.CharField(verbose_name="การสอบสวน", max_length=1, choices=InspectChoices.choices, default=InspectChoices.START_INVESTIGATION, null=True, blank=True)

    initial_likelihood = models.IntegerField(verbose_name="โอกาสเริ่มต้น", choices=LikelihoodChoices.choices, default=LikelihoodChoices.RARE, null=True, blank=True)
    initial_severity = models.IntegerField(verbose_name="ความรุนแรงเริ่มต้น", choices=SeverityChoices.choices, default=SeverityChoices.MINOR, null=True, blank=True)
    initial_risk_level = models.IntegerField(verbose_name="ระดับความเสี่ยงเริ่มต้น", validators=[MinValueValidator(1), MaxValueValidator(25)], null=True, blank=True)

    residual_likelihood = models.IntegerField(verbose_name="โอกาสหลังแก้ไข",choices=LikelihoodChoices.choices, null=True, blank=True)
    residual_severity = models.IntegerField(verbose_name="ความรุนแรงหลังแก้ไข", choices=SeverityChoices.choices, null=True, blank=True)
    residual_risk_level = models.IntegerField(verbose_name="ระดับความเสี่ยงหลังแก้ไข", validators=[MinValueValidator(1), MaxValueValidator(25)], null=True, blank=True)

    source = models.ManyToManyField(HazardSource, verbose_name="แหล่งที่มา", blank=True)
    related_report = models.ForeignKey('Report.BaseReport', verbose_name="รายงานที่เกี่ยวข้อง", related_name="hazard_log", on_delete=models.SET_NULL, null=True, blank=True)
    note = models.TextField(verbose_name="หมายเหตุ", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = verbose_name_plural = "1. ทะเบียนความเสี่ยง"
        permissions = [
            ("view_all_hazard_log", "*ดูทะเบียนความเสี่ยงทั้งหมดได้"),
            ("view_affiliation_hazard_log", "*ดูทะเบียนความเสี่ยงของหน่วยตนเองได้"),
            ("create_hazard_log", "*สร้างทะเบียนความเสี่ยงได้"),
            ("edit_hazard_log", "*แก้ไขทะเบียนความเสี่ยงได้"),
            ("delete_hazard_log", "*ลบทะเบียนความเสี่ยงได้"),
            ("detail_hazard_log", "*ดูรายละเอียดทะเบียนความเสี่ยงได้"),
            
            ("create_cap", "*สร้าง CAP ได้"),
        ]

    def __str__(self):
        return f"{self.code} - {self.category.event.name}"
    
    def get_absolute_url(self):
        return reverse("risk_management:hazard-detail", kwargs={"id": self.pk})
    
    def save(self, *args, **kwargs):
        if self.id is None and not self.code:
            self.serial_number = (HazardLog.objects.aggregate(Max('serial_number'))['serial_number__max'] or 0) + 1
            self.code = f"HZ{self.serial_number:04d}"
            
        self.initial_risk_level = (self.initial_likelihood or 1) * (self.initial_severity or 1)
        self.residual_risk_level = (self.residual_likelihood or 1) * (self.residual_severity or 1)
        super().save(*args, **kwargs)
        


class CAP(models.Model):
    order = models.PositiveIntegerField(verbose_name="ลำดับ", blank=True, null=True)
    hazard_log = models.ForeignKey(HazardLog, verbose_name="Hazard Log", on_delete=models.CASCADE, related_name="caps")
    title = models.CharField(verbose_name="หัวข้อ", max_length=255, null=False, blank=False)
    description = models.TextField(verbose_name="รายละเอียด", null=True, blank=True)
    
    assign_to  = models.CharField(verbose_name="ผู้รับผิดชอบ", max_length=255, null=True, blank=True)
    status = models.CharField(verbose_name="สถานะ", max_length=2, choices=CAPStatusChoices.choices, default=CAPStatusChoices.PLANNING, null=True, blank=True)

    due_date = models.DateField(verbose_name="วันครบกำหนด", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = verbose_name_plural = "3. Corrective Action Plan (CAP)"
        ordering = ['order', 'due_date']

    def __str__(self):
        return f"{self.title} ({self.status})"