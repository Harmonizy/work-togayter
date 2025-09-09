from django.db import models

# from ckeditor.fields import RichTextField

from .choices import RegionChoices
from common.RTAFUser.models import Affiliation, Squadron

class Event(models.Model):
    name = models.CharField(verbose_name="ชื่อ", max_length=120)
    hazard_title = models.CharField(verbose_name="หัวข้อทะเบียนความเสี่ยง", max_length=120, blank=True, null=True)

    class Meta:
        verbose_name = verbose_name_plural = "1. เหตุการณ์"

    def __str__(self):
        return self.name


class AircraftType(models.Model):
    name = models.CharField(verbose_name="ชื่อ", max_length=120)

    class Meta:
        verbose_name = verbose_name_plural = "2.1 ประเภทอากาศยาน"

    def __str__(self):
        return self.name


class Aircraft(models.Model):
    name = models.CharField(verbose_name="แบบ บ.", max_length=60)
    name_en = models.CharField(verbose_name="แบบ บ.(ENG)", max_length=120, blank=True, null=True)
    affiliation_fk = models.ForeignKey("RTAFUser.Affiliation", verbose_name="กองบิน",related_name="aircrafts_fk",on_delete=models.CASCADE, blank=True, null=True)
    squadron = models.ForeignKey("RTAFUser.Squadron", verbose_name="ฝูงบิน", related_name="aircrafts",on_delete=models.CASCADE, blank=True, null=True)
    type = models.ManyToManyField("Data.AircraftType", verbose_name="ประเภท", related_name="aircrafts", blank=True)

    class Meta:
        verbose_name = verbose_name_plural = "2. อากาศยาน"

    def __str__(self):
        return self.name
    

class AircraftSystem(models.Model):
    name = models.CharField(verbose_name="ชื่อ", max_length=120)

    class Meta:
        verbose_name = verbose_name_plural = "3. ระบบอากาศยาน"

    def __str__(self):
        return self.name


class FlightPhase(models.Model):
    name = models.CharField(verbose_name="ชื่อ", max_length=120)

    class Meta:
        verbose_name = verbose_name_plural = "4. ช่วงของการบิน"

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(verbose_name="ชื่อ", max_length=255)
    region = models.CharField(verbose_name="ภูมิภาค", max_length=2, choices=RegionChoices.choices)
    is_airforce = models.BooleanField(verbose_name="ที่ ทอ.", default=False)
    
    latitude = models.FloatField(verbose_name="ละติจูด", null=True, blank=True)
    longitude = models.FloatField(verbose_name="ลองจิจูด", null=True, blank=True)
    
    class Meta:
        verbose_name = verbose_name_plural = "5. สถานที่"

    def __str__(self):
        return self.name
    

class GroundSafetyCategory(models.Model):
    order = models.PositiveIntegerField(verbose_name="ลำดับ", default=0)
    name = models.CharField(verbose_name="ชื่อ", max_length=120)

    class Meta:
        verbose_name = verbose_name_plural = "6. สาขานิรภัย (ภาคพื้น)"
        ordering = ['order',]

    def __str__(self):
        return self.name


class Keyword(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "7. คำสำคัญ"
        verbose_name_plural = "7. คำสำคัญ"

    def __str__(self):
        return self.name