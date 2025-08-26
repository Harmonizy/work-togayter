from django.db import models

class DataStatus(models.TextChoices):
    HRIS = 'H', 'HRIS'
    SELF = 'S', 'กรอกเอง'
    ADMIN = 'A', 'Admin'
    EXTENSION = 'E', 'ผ่อนผัน'
    

