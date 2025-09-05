from django.db import models

class HazardLogStatusChoices(models.TextChoices):
    OPEN = 'O', 'เปิด'
    CLOSE = 'C', 'ปิด'


class InspectChoices(models.TextChoices):
    START_INVESTIGATION = 'S', 'เริ่มการสอบสวน'
    DATA_CAPTURE_ONLY = 'D', 'เก็บข้อมูล'


class CAPStatusChoices(models.TextChoices):
    PLANNING = 'P', 'วางแผน'
    IN_PROGRESS = 'I', 'กำลังดำเนินการ'
    COMPLETE = 'C', 'เสร็จสิ้น'
