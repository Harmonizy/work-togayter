from django.db import models

# from ckeditor.fields import RichTextField

from .choices import RegionChoices


class Event(models.Model):
    name = models.CharField(verbose_name="ชื่อ", max_length=120)

    class Meta:
        verbose_name = verbose_name_plural = "1. เหตุการณ์"

    def __str__(self):
        return self.name


class Aircraft(models.Model):
    model = models.CharField(verbose_name="รุ่น", max_length=20)
    name = models.CharField(verbose_name="ชื่อ", max_length=60)

    class Meta:
        verbose_name = verbose_name_plural = "2. อากาศยาน"

    def __str__(self):
        return self.name
    

class AircraftSystem(models.Model):
    name = models.CharField(verbose_name="ชื่อ", max_length=120)

    class Meta:
        verbose_name = verbose_name_plural = "2. ระบบอากาศยาน"

    def __str__(self):
        return self.name


class FlightPhase(models.Model):
    name = models.CharField(verbose_name="ชื่อ", max_length=120)

    class Meta:
        verbose_name = verbose_name_plural = "3. ช่วงของการบิน"

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(verbose_name="ชื่อ", max_length=255)
    region = models.CharField(verbose_name="ภูมิภาค", max_length=2, choices=RegionChoices.choices)
    is_airforce = models.BooleanField(verbose_name="ที่ ทอ.", default=False)
    
    latitude = models.FloatField(verbose_name="ละติจูด", null=True, blank=True)
    longitude = models.FloatField(verbose_name="ลองจิจูด", null=True, blank=True)
    
    class Meta:
        verbose_name = verbose_name_plural = "4. สถานที่"

    def __str__(self):
        return self.name
    

class GroundSafetyCategory(models.Model):
    order = models.PositiveIntegerField(verbose_name="ลำดับ", default=0)
    name = models.CharField(verbose_name="ชื่อ", max_length=120)

    class Meta:
        verbose_name = verbose_name_plural = "5. สาขานิรภัย (ภาคพื้น)"
        ordering = ['order',]

    def __str__(self):
        return self.name


class Keyword(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "6. คำสำคัญ"
        verbose_name_plural = "6. คำสำคัญ"

    def __str__(self):
        return self.name