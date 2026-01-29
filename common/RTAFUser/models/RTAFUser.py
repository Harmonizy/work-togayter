from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser, Group


from .mixins import RTAFUserMixins
from .validators import validate_person_id, validate_af_id
from .choices import DataStatus

Group.add_to_class('description', models.CharField(max_length=180,null=True, blank=True))

class Rank(models.Model):
    id = models.IntegerField(primary_key=True)
    short_name = models.CharField(verbose_name="ชื่อย่อ", max_length=15)
    full_name = models.CharField(verbose_name="ชื่อเต็ม", max_length=30, null = True, blank = True)
    eng_short_name = models.CharField(verbose_name="ชื่อย่อ (อังกฤษ)", max_length=15, null = True, blank = True)
    eng_full_name = models.CharField(verbose_name="ชื่อเต็ม (อังกฤษ)", max_length=30, null = True, blank = True)
    level = models.IntegerField(verbose_name="ระดับ", null = True, blank = True)
    short_display = models.CharField(verbose_name="แสดงชื่อย่อ", max_length=15, null = True, blank = True)
    is_airforce = models.BooleanField(verbose_name="ทหารอากาศ", default=True, null = True, blank = True)

    class Meta:        
        verbose_name_plural = "1. ยศทหาร"
        ordering = ['-level', 'id']

    def __str__(self):
        return self.short_name


class AffiliationAircraft(models.Model):
    affiliation = models.ForeignKey('Affiliation', verbose_name="สังกัด", on_delete=models.CASCADE, limit_choices_to={"is_airbase": True})
    aircraft = models.ForeignKey('Data.Aircraft', verbose_name="ประเภทอากาศยาน", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "5. อากาศยานประจำฝูงบิน"


class Affiliation(models.Model):
    hris_code = models.CharField(verbose_name="รหัส HRIS", max_length=10, null=True, blank = True)
    short_name = models.CharField(verbose_name="ชื่อย่อ", max_length=20, null=True, blank = True)
    full_name = models.CharField(verbose_name="ชื่อเต็ม", max_length=255, null=True, blank = True)
    
    is_rtaf_directed = models.BooleanField(verbose_name="นขต.ทอ.", default=True, null=True, blank = True)
    is_airbase = models.BooleanField(verbose_name="ฐานบิน", default=False, null=True, blank = True)
    
    super_affiliation = models.ForeignKey('self', verbose_name="ต้นสังกัด", on_delete=models.SET_NULL, null = True, blank = True)
    airviation_content = models.TextField(verbose_name="ร่างเนื้อหารายงานการบิน", null=True, blank=True)
    officer_content = models.TextField(verbose_name="ร่างเนื้อหาผู้บังคับบัญชาด้านความปลอดภัย", null=True, blank=True)

    aircraft_types = models.ManyToManyField('Data.Aircraft', verbose_name="อากาศยานบที่มี", through=AffiliationAircraft, blank=True)

    class Meta:
        verbose_name_plural = "2. สังกัด"
        ordering = ['short_name']

    def __str__(self):
        return self.short_name


class RTAFUser(RTAFUserMixins, AbstractUser):
    af_id = models.CharField(verbose_name="เลข ขรก.", max_length=12, null=True, blank=True, validators=[validate_af_id])
    person_id = models.CharField(verbose_name="เลข ปชช.", max_length=13, null=True, blank=True, validators=[validate_person_id])
    rank = models.ForeignKey(Rank, verbose_name="ยศ/คำนำหน้า",  on_delete=models.SET_NULL, limit_choices_to={"is_airforce" : True}, null=True, blank=True)
    position = models.CharField(verbose_name="ตำแหน่ง (ย่อ)", max_length=255, null = True, blank = True)    
    affiliation = models.ForeignKey(Affiliation, verbose_name="สังกัด", on_delete=models.SET_NULL, null = True, blank=True, related_name='staff')
    work_affiliation = models.ForeignKey(Affiliation, verbose_name="ปฏิบัติงานที่", on_delete=models.SET_NULL, null = True, blank=True, related_name='work_staff') 
    
    fetch_hris = models.BooleanField(verbose_name="Load ข้อมูลจาก HRIS", default=True)

    class Meta:
        verbose_name_plural = "3. ผู้ใช้งานระบบ"
        ordering = ['-rank__level', 'first_name']
        permissions = [
            ("add_report", "Can create hazard/incident/BBS report"),
            ("view_hazard_log", "Can view hazard log"),
            ("assess_risk", "Can perform risk assessment"),
            ("manage_cap", "Can create, update, and close CAP"),
            ("verify_cap", "Can verify CAP"),
            ("access_investigation", "Can access accident investigation module"),
            ("manage_evidence", "Can view and manage evidence in oversight cases"),
        ]
    def __str__(self):
        return self.get_full_name()


class Squadron(models.Model):
    code = models.CharField(verbose_name="รหัสฝูง", max_length=10, null=True, blank = True)  # เช่น 403
    nickname = models.CharField(verbose_name="Callsign", max_length=50, null=True, blank = True) 
    affiliation = models.ForeignKey(Affiliation, verbose_name="สังกัด", limit_choices_to={"is_airbase": True}, on_delete=models.SET_NULL, null=True, blank=True)

    latitude = models.FloatField(verbose_name="ละติจูด", null=True, blank=True)
    longitude = models.FloatField(verbose_name="ลองจิจูด", null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = "4. ฝูงบิน"
        ordering = ['code']

    def __str__(self):
        return f"{self.code}({self.affiliation})"

