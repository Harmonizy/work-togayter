import os
from datetime import datetime

from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from .reports import BaseReport
from common.RTAFUser.models import RTAFUser

class BaseContentType(models.Model):
    base_report = models.ForeignKey(BaseReport, on_delete=models.CASCADE, related_name='%(class)s_attachment', null=False, blank=False)

    comment = models.CharField(verbose_name="หมายเหตุ", max_length=120, null=True, blank=True)
    recorder = models.ForeignKey(RTAFUser, verbose_name="ผู้บันทึก", on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สร้าง")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="วันที่แก้ไข")


    class Meta:
        # app_label = "Attachment"
        abstract = True
        
        
def get_upload_to(instance, filename):
    if isinstance(instance, Image):
        base_folder = 'images'
    elif isinstance(instance, File):
        base_folder = 'files'
    elif isinstance(instance, Recommendation):
        base_folder = 'recommendations'
    else:
        base_folder = 'attachments' 
        
    affiliation = getattr(instance.base_report, 'affiliation', 'default_affiliation')
    fiscal_year = getattr(instance.base_report, 'fiscal_year', 'default')
    current_month = datetime.now().strftime('%m')
    return os.path.join(f"attachments/{affiliation}/{base_folder}/{fiscal_year}/{current_month}/", filename)


class Image(BaseContentType):
    image = models.ImageField(verbose_name="รูปภาพ", upload_to=get_upload_to)

    def __str__(self):
        return f"Image"


class Recommendation(BaseContentType):
    note = models.TextField(verbose_name="คำแนะนำ")

    def __str__(self):
        return f"Recommendation"


class File(BaseContentType):
    file = models.FileField(verbose_name="ไฟล์", upload_to=get_upload_to)

    def __str__(self):
        return f"File"
