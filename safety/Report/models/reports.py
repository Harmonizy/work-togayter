from datetime import date

from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import reverse
# from django.contrib.contenttypes.fields import GenericRelation

# from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField

from ..choices import ( BaseReportTypeChoices, ReportTypeChoices, DamageTypeChoices, InjuryLevelChoices, ReportStatusChoices, OrganizationExpectationChoice, PriorityChoices, RoleTypeChoices, AccidentTypeChoices)
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
        

class BaseReport(models.Model):
    fiscal_year = models.IntegerField(verbose_name="ปีงบประมาณ",default=current_fiscal_year)
    affiliation = models.ForeignKey(Affiliation,verbose_name="หน่วยงาน",on_delete=models.SET_NULL,null=True,blank=True)
    event_date = models.DateField(verbose_name="วันที่เกิดเหตุ",default=date.today)
    event_time = models.TimeField(verbose_name="เวลาเกิดเหตุ",default=timezone.now)

    report_type = models.CharField(verbose_name="ประเภทรายงาน",max_length=2,choices=ReportTypeChoices.choices,default=ReportTypeChoices.SIMPLE)
    priority = models.CharField(verbose_name="ความสำคัญ",max_length=1,choices=PriorityChoices.choices,null=True,blank=True)
    status = models.IntegerField(verbose_name="สถานะ",choices=ReportStatusChoices.choices,default=ReportStatusChoices.DRAFT)

    title = models.CharField(verbose_name="หัวข้อรายงาน",max_length=255)
    content = RichTextField(verbose_name="เนื้อหา", null=True, blank=True)
    
    first_recommendation = models.TextField(verbose_name="คำแนะนำเบื้องต้น",null=True,blank=True)
    initial_action_taken = models.TextField(verbose_name="การแก้ไขที่ดำเนินการ",null=True,blank=True)
    
    recorder = models.ForeignKey(RTAFUser,verbose_name="ผู้บันทึก",on_delete=models.CASCADE,null=True,blank=True)
    anonymous = models.BooleanField(verbose_name="ไม่ระบุชื่อผู้บันทึก",default=False)
    comment = models.CharField(verbose_name="หมายเหตุ",max_length=120,null=True,blank=True)
    
    created_at = models.DateTimeField(verbose_name="วัน-เวลาที่สร้างรายงาน",auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="วัน-เวลาที่แก้ไขล่าสุด",auto_now=True)
    
    # objects = models.Manager()
    objects = ReportManager()
    
    class Meta:
        verbose_name = verbose_name_plural = "1. แบบรายงาน"
        permissions = [
            ("create_safety_report", "สร้างรายงานนิรภัยได้"),
        ]

    def __str__(self):
        return self.title


class BaseAbsoluteURL:
    
    def __str__(self):
        return self.base_report.title
        
    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})


class GroundReport(BaseAbsoluteURL, models.Model):
    base_report = models.OneToOneField(BaseReport, on_delete=models.CASCADE, primary_key=True)
    location = models.CharField(verbose_name="สถานที่โดยละเอียด", max_length=255, null=True, blank=True,
                                help_text="ระบุสถานที่เกิดเหตุอย่างละเอียด เช่น โรงซ่อมอากาศนายที่ 3 แผนกซ่อมอากาศยานฯ")
    category = models.ForeignKey(GroundSafetyCategory, verbose_name="สาขา", on_delete=models.CASCADE, null=True, blank=True)
    accident_type = models.IntegerField(verbose_name="ประเภทอุบัติเหตุ", choices=AccidentTypeChoices.choices, null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = "2. ภาคพื้น"


class AviationReport(BaseAbsoluteURL, models.Model):
    base_report = models.OneToOneField(BaseReport, on_delete=models.CASCADE, primary_key=True)

    squadron = models.ForeignKey(Squadron, verbose_name="หน่วยบิน", on_delete=models.CASCADE, null=True, blank=True)
    aircraft = models.ForeignKey(Aircraft, verbose_name="อากาศยาน", on_delete=models.CASCADE, null=True, blank=True)
    system = models.ManyToManyField(AircraftSystem, verbose_name="ระบบอากาศยาน", related_name='aviation_reports', blank=True)
    flight_phase = models.ManyToManyField('Data.FlightPhase', verbose_name="ช่วงของการบิน", related_name='aviation_reports', blank=True)
    plane_number = models.CharField(verbose_name="เลขที่เครื่องบิน", null=True, blank=True)
    air_control = models.CharField(verbose_name="หน่วยควบคุมการจราจรทางอากาศ", null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = "3. ภาคอากาศ"


class Participant(models.Model):
    base_report = models.ForeignKey(BaseReport, on_delete=models.CASCADE, related_name='participants')
    full_name = models.CharField(verbose_name="ชื่อ-นามสกุล", null=True, blank=True)
    role = models.ForeignKey(Role, verbose_name="บทบาท", on_delete=models.SET_NULL, null=True, blank=True)
    injury_level = models.IntegerField(verbose_name="ระดับการบาดเจ็บ", choices=InjuryLevelChoices.choices, null=True, blank=True)
    note = models.TextField(verbose_name="หมายเหตุ", null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = "4. บุคคล"


# class ObservationReport(BaseAbsoluteURL, models.Model):
#     base_report = models.OneToOneField(BaseReport, on_delete=models.CASCADE, primary_key=True)

#     behavior = models.IntegerField(verbose_name="พฤติกรรม", choices=OrganizationExpectationChoice.choices, null=True, blank=True)

#     class Meta:
#         verbose_name = verbose_name_plural = "รายงานอุบัติเหตุ/อุบัติการณ์"