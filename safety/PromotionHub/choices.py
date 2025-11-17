from django.db import models

class PromotionStatusChoices(models.TextChoices):
    DRAFT = 'D', 'ร่าง'
    PUBLISHED = 'P', 'เผยแพร่'
    ARCHIVED = 'A', 'เก็บถาวร'

class PromotionPublishChoices(models.TextChoices):
    AIRFORCE = 'A', 'ทอ.'
    UNIT = 'U', 'หน่วย'
    NONE = 'N', 'ไม่ระบุ'
