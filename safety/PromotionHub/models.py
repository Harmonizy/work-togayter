from django.db import models

from .choices import PromotionStatusChoices, PromotionPublishChoices
from common.RTAFUser.models.RTAFUser import RTAFUser, Affiliation
from common.Services.super_app_api import send_notification

class Quiz(models.Model):
    title = models.CharField(verbose_name="หัวข้อ", max_length=255)
    description = models.TextField(verbose_name="รายละเอียด", blank=True, null=True)

    class Meta:
        verbose_name = verbose_name_plural = "4. แบบทดสอบ"

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, verbose_name="แบบทดสอบ", on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(verbose_name="คำถาม")

    class Meta:
        verbose_name = verbose_name_plural = "5. คําถาม"

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, verbose_name="แบบทดสอบ", on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(verbose_name="ตัวเลือก", max_length=255)
    is_correct = models.BooleanField(verbose_name="ถูกต้อง", default=False)

    class Meta:
        verbose_name = verbose_name_plural = "6. ตัวเลือก"

    def __str__(self):
        return self.text


class QuizResult(models.Model):
    quiz = models.ForeignKey(Quiz, verbose_name="แบบทดสอบ", on_delete=models.CASCADE)
    user = models.ForeignKey(RTAFUser, verbose_name="ผู้เข้าชม", on_delete=models.SET_NULL, null=True, blank=True)
    score = models.FloatField(verbose_name="คะแนน", default=0)
    completed_at = models.DateTimeField(verbose_name="วันที่สําเร็จ", auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = "3. ผลการทดสอบ"

    def __str__(self):
        return f"{self.user} - {self.score}"


class Promotion(models.Model):
    image = models.ImageField(verbose_name="รูปภาพ", upload_to='safety_promotion/')
    title = models.CharField(verbose_name="หัวข้อ", max_length=255)
    content = models.TextField(verbose_name="เนื้อหา")
    status = models.CharField(verbose_name="สถานะ", max_length=1, choices=PromotionStatusChoices.choices, default=PromotionStatusChoices.DRAFT, null=True, blank=True)
    publish = models.CharField(verbose_name="เผยแพร่", max_length=1, choices=PromotionPublishChoices.choices, default=PromotionPublishChoices.AIRFORCE, null=True, blank=True)

    quiz = models.ForeignKey(Quiz, verbose_name="แบบทดสอบ", on_delete=models.SET_NULL, null=True, blank=True)

    user = models.ForeignKey(RTAFUser, verbose_name="ผู้สร้าง", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name="วันที่สร้าง", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="วันที่แก้ไข", auto_now=True)

    class Meta:
        verbose_name = verbose_name_plural = "1. ประชาสัมพันธ์"
        permissions = [
            
        ]

    def __str__(self):
        return self.title

    def send_notify(self, user_list : list):
        send_notification(title=self.title, message=self.content, user_ids=user_list)


class PromotionView(models.Model):
    user = models.ForeignKey(RTAFUser, verbose_name="ผู้เข้าชม", on_delete=models.SET_NULL, null=True, blank=True)
    promotion = models.ForeignKey(Promotion, verbose_name="โปรโมชั่น", on_delete=models.SET_NULL, null=True, blank=True)
    viewed_at = models.DateTimeField(verbose_name="วันที่เข้าชม", auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = "2. การเข้าชม"

    def __str__(self):
        return f"{self.user} - {self.promotion}"
    


