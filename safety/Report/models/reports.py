from datetime import date

from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import reverse
# from django.contrib.contenttypes.fields import GenericRelation

# from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField

from ..choices import (TypeChoices, ReportTypeChoices, DamageTypeChoices, InjuryLevelChoices, ReportStatusChoices, OrganizationExpectationChoice, PriorityChoices, RoleTypeChoices, AccidentTypeChoices, GroundSafetyCategoryChoices)
from safety.Data.models import Event, Aircraft, AircraftSystem, FlightPhase, Location, GroundSafetyCategory, Keyword, Role
from common.RTAFUser.models import RTAFUser, Affiliation, Squadron

def current_fiscal_year():
    today = timezone.now()
    if today.month >= 10:
        return (today.year + 1 + 543) % 100
    return (today.year + 543) % 100


class ReportManager(models.Manager):
    def for_user(self, user):
        if user.groups.filter(name__in=['Administrator','SafetyCenterOfficer', 'TopRTAFExecutive']).exists():
            return self.all()
        elif user.groups.filter(name__in=['SafetyOfficer']).exists():
            return self.filter(Q(affiliation=user.affiliation) | Q(recorder=user))
        else:
            return self.filter(recorder=user)


class ReportType(models.Model):
    value = models.CharField(max_length=4,unique=True,verbose_name="รหัสประเภทรายงาน")
    label = models.CharField(max_length=255,verbose_name="ชื่อประเภทรายงาน")
    type = models.CharField(max_length=1,choices=TypeChoices.choices,default=TypeChoices.GROUND,verbose_name="กลุ่มรายงาน")
    is_active = models.BooleanField(default=True,verbose_name="เปิดใช้งาน")
    order = models.PositiveSmallIntegerField(default=0,verbose_name="ลำดับการแสดงผล")

    class Meta:
        verbose_name = verbose_name_plural = "2. ประเภทรายงาน"
        ordering = ["type", "order", "value"]

    def __str__(self):
        return f"{self.value} - {self.label}"


class BaseReport(models.Model):
    fiscal_year = models.IntegerField(verbose_name="ปีงบประมาณ", default=current_fiscal_year)
    affiliation = models.ForeignKey(Affiliation,verbose_name="หน่วยรับผิดชอบ", related_name='base_reports', on_delete=models.SET_NULL, null=True, blank=True, help_text="หน่วยงานหลักที่รับผิดชอบ")
    location_affiliation = models.ForeignKey(Affiliation,verbose_name="หน่วยที่เกิดเหตุ",related_name='location_base_reports', on_delete=models.SET_NULL, null=True, blank=True, help_text="หน่วยงานที่อยู่ในสถานที่เกิดเหตุ")
    event_date = models.DateField(verbose_name="วันที่เกิดเหตุ", default=date.today)
    event_time = models.TimeField(verbose_name="เวลาเกิดเหตุ", default=timezone.now)

    report_type = models.CharField(verbose_name="ประเภทรายงาน", max_length=4, choices=ReportTypeChoices.choices, default=ReportTypeChoices.SIMPLE)
    priority = models.CharField(verbose_name="ความสำคัญ", max_length=1, choices=PriorityChoices.choices)
    status = models.IntegerField(verbose_name="สถานะ", choices=ReportStatusChoices.choices, default=ReportStatusChoices.DRAFT)

    title = models.CharField(verbose_name="หัวข้อรายงาน", max_length=255)
    content = RichTextField(verbose_name="เนื้อหา", null=True, blank=True)
    
    first_recommendation = models.TextField(verbose_name="คำแนะนำเบื้องต้น", null=True, blank=True)
    initial_action_taken = models.TextField(verbose_name="การแก้ไขที่ดำเนินการ", null=True, blank=True)

    recorder = models.ForeignKey(RTAFUser,verbose_name="ผู้บันทึก", on_delete=models.CASCADE,null=True, blank=True)
    anonymous = models.BooleanField(verbose_name="ไม่ระบุชื่อผู้บันทึก", default=False)
    comment = models.CharField(verbose_name="หมายเหตุ",max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(verbose_name="วัน-เวลาที่สร้างรายงาน", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="วัน-เวลาที่แก้ไขล่าสุด", auto_now=True)

    objects = ReportManager()
    
    class Meta:
        verbose_name = verbose_name_plural = "1. แบบรายงาน"
        permissions = [
            ("view_all_report_list", "*ดูรายงานทั้งหมดได้"),
            ("view_affiliation_report_list", "*ดูรายงานของหน่วยงานตนเองได้"),
            ("create_report", "*สร้างรายงานละเอียดได้"),
            ("edit_report", "*แก้ไขรายงานได้"),
            ("delete_report", "*ลบรายงานได้"),
            ("view_all_report_detail", "*ดูรายละเอียดรายงานทั้งหมดได้"),
            ("view_affiliation_report_detail", "*ดูรายละเอียดรายงานของหน่วยงานตัวเองได้"),
            ("approve_report", "*อนุมัติรายงานได้"),

            ("create_sixA", "*ประเมิน 6A ได้"),

            ("view_all_dashboard", "*ดูสถิติทั้งหมดได้"),
            ("view_affiliation_dashboard", "*ดูสถิติของหน่วยงานตัวเองได้"),
        ]

    def __str__(self):
        return f"{self.id}: {self.title}"
    
    def save(self, *args, **kwargs):
        if self.event_time:
            self.event_time = self.event_time.replace(second=0, microsecond=0)
        super().save(*args, **kwargs)


class BaseAbsoluteURL:
    def __str__(self):
        return self.base_report.title
        
    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})


class GroundReport(BaseAbsoluteURL, models.Model):
    base_report = models.OneToOneField(BaseReport, on_delete=models.CASCADE, primary_key=True)
    location = models.CharField(verbose_name="สถานที่โดยละเอียด", max_length=255, null=True, blank=True,
                                help_text="ระบุสถานที่เกิดเหตุอย่างละเอียด เช่น โรงซ่อมอากาศนายที่ 3 แผนกซ่อมอากาศยานฯ")
    category = models.IntegerField(verbose_name="สาขา", choices=GroundSafetyCategoryChoices.choices, default=GroundSafetyCategoryChoices.GENERAL, null=True, blank=True)
    accident_type = models.IntegerField(verbose_name="ประเภทอุบัติเหตุ", choices=AccidentTypeChoices.choices, null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = "1.1 ภาคพื้น"


class AviationReport(BaseAbsoluteURL, models.Model):
    base_report = models.OneToOneField(BaseReport, on_delete=models.CASCADE, primary_key=True)

    squadron = models.ForeignKey(Squadron, verbose_name="หน่วยบิน", on_delete=models.CASCADE, null=True, blank=True)
    aircraft = models.ForeignKey(Aircraft, verbose_name="อากาศยาน", on_delete=models.CASCADE, null=True, blank=True)
    system = models.ManyToManyField(AircraftSystem, verbose_name="ระบบอากาศยาน", related_name='aviation_reports', blank=True)
    flight_phase = models.ManyToManyField('Data.FlightPhase', verbose_name="ช่วงของการบิน", related_name='aviation_reports', blank=True)
    plane_number = models.CharField(verbose_name="เลขที่เครื่องบิน", null=True, blank=True)
    air_control = models.CharField(verbose_name="หน่วยควบคุมการจราจรทางอากาศ", null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = "1.2 การบิน"


class Participant(models.Model):
    base_report = models.ForeignKey(BaseReport, on_delete=models.CASCADE, related_name='participants')
    full_name = models.CharField(verbose_name="ชื่อ-นามสกุล", null=True, blank=True)
    role = models.ForeignKey(Role, verbose_name="บทบาท", on_delete=models.SET_NULL, null=True, blank=True)
    injury_level = models.IntegerField(verbose_name="ระดับการบาดเจ็บ", choices=InjuryLevelChoices.choices, null=True, blank=True)
    note = models.TextField(verbose_name="หมายเหตุ", null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = "1.3 บุคคลเกี่ยวข้อง"


class ReferenceReport(models.Model):
    base_report = models.ForeignKey(BaseReport, on_delete=models.CASCADE, related_name='references')
    report = models.ForeignKey(BaseReport, verbose_name="รายงาน", on_delete=models.CASCADE, null=True, blank=True)
    note = models.TextField(verbose_name="หมายเหตุ", null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = "1.4 รายงานอ้างอิง"


# class ObservationReport(BaseAbsoluteURL, models.Model):
#     base_report = models.OneToOneField(BaseReport, on_delete=models.CASCADE, primary_key=True)

#     behavior = models.IntegerField(verbose_name="พฤติกรรม", choices=OrganizationExpectationChoice.choices, null=True, blank=True)

#     class Meta:
#         verbose_name = verbose_name_plural = "รายงานอุบัติเหตุ/อุบัติการณ์"