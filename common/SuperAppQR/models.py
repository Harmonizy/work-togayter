import json
import base64
import random
import string

from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

SUPER_APP_QR_PREFIX = settings.SUPER_APP_QR_PREFIX

User = get_user_model()


    
class QRType(models.Model):
    name = models.CharField(verbose_name="ชื่อ QR", max_length=100, unique=True, help_text="ชื่อที่ใช้ระบุประเภทของ QR Code", blank=False, null=False)
    description = models.TextField(verbose_name="คำอธิบาย", blank=True, null=True)
    url_redirect = models.CharField(verbose_name="URL Redirect", max_length=255, blank=False, null=False, help_text="URL ที่จะ redirect เมื่อสแกน QR Code นี้")
    object_id_name = models.CharField(verbose_name="Object ID Param Name", max_length=20, blank=True, null=True)
    keys = models.JSONField(verbose_name="Keys", blank=True, null=True, help_text="Keys เพื่อ map กับ arguments")
    
    create_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_qrtypes')
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = "1. ประเภท QR Code"
        ordering = ['-create_at']
        
    def __str__(self):
        return self.name


class QRImageData(models.Model):    
    type = models.ForeignKey(QRType, on_delete=models.CASCADE, related_name='qr_images')    
    object_id = models.PositiveIntegerField(verbose_name="Object ID", null=True, blank=True, help_text="ID ของ object ที่เกี่ยวข้อง เช่น ID ของผู้ใช้ หรือ ID ของรายการอื่นๆ")
    token = models.CharField(verbose_name="Token", max_length=4)
    args = models.JSONField(verbose_name="Arguments", blank=True, null=True, help_text="Arguments อื่น ๆ")

    class Meta:
        verbose_name = verbose_name_plural = "2. ข้อมูล ยิง QR Code"
        unique_together = ('type', 'object_id')
        ordering = ['-id']
        
    def __str__(self):
        return f"QRImageData {self.id}"
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = "".join(random.choices(string.ascii_letters + string.digits, k=4))
            while QRImageData.objects.filter(token=self.token).exists():
                self.token = "".join(random.choices(string.ascii_letters + string.digits, k=4))
                
        super().save(*args, **kwargs)
    
    def qr_text(self):
        print(f"{SUPER_APP_QR_PREFIX}{self.token}")
        return f"{SUPER_APP_QR_PREFIX}{self.token}"


class QRScan(models.Model):
    qr_image_data = models.ForeignKey(QRImageData, on_delete=models.CASCADE, related_name='scans')
    scanner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='qr_scans')
    scan_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = "3. Logs"
        ordering = ['-scan_time']
        
    def __str__(self):
        return f"Scan of {self.qr_image_data.id} by {self.scanner}"
