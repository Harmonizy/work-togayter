from django.utils.html import strip_tags
from django.db import models


from .choices import PromotionStatusChoices, PromotionPublishChoices, PromotionPriorityChoices, PromotionTypeChoices
from common.RTAFUser.models.RTAFUser import RTAFUser, Affiliation
from common.Services.super_app_api import send_notification

import mimetypes
from ckeditor.fields import RichTextField
from tinymce.models import HTMLField

class Quiz(models.Model):
    title = models.CharField(verbose_name="หัวข้อ", max_length=255)
    description = models.TextField(verbose_name="รายละเอียด", blank=True, null=True)

    class Meta:
        verbose_name = verbose_name_plural = "4. แบบทดสอบ"

    def __str__(self):
        return self.title

    @property
    def num_completed(self):
        return QuizResult.objects.filter(quiz=self).count()


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
        verbose_name = verbose_name_plural = "5.5 ตัวเลือก"

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
    title = models.CharField(verbose_name="หัวข้อ", max_length=255)
    content = RichTextField(verbose_name="เนื้อหา", null=True, blank=True)
    status = models.CharField(verbose_name="สถานะ", max_length=1, choices=PromotionStatusChoices.choices, default=PromotionStatusChoices.DRAFT, null=True, blank=True)
    publish = models.CharField(verbose_name="เผยแพร่", max_length=1, choices=PromotionPublishChoices.choices, default=PromotionPublishChoices.NONE, null=True, blank=True)
    priority = models.CharField(verbose_name="ความสำคัญ", max_length=1, choices=PromotionPriorityChoices.choices, default=PromotionPriorityChoices.NONE, null=True, blank=True)
    type = models.CharField(verbose_name="ประเภท", max_length=1, choices=PromotionTypeChoices.choices, default=PromotionTypeChoices.NONE, null=True, blank=True)
    
    quiz = models.ForeignKey(Quiz, verbose_name="แบบทดสอบ", on_delete=models.SET_NULL, null=True, blank=True)
    
    user = models.ForeignKey(RTAFUser, verbose_name="ผู้สร้าง", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name="วันที่สร้าง", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="วันที่แก้ไข", auto_now=True)

    num_view = models.IntegerField(verbose_name="จํานวนการเข้าชม", default=0)

    class Meta:
        verbose_name = verbose_name_plural = "1. ประชาสัมพันธ์"
        permissions = [
            ("view_all_promotion_hub", "*ดูการประชาสัมพันธ์ทั้งหมดได้"),
            ("view_affiliation_promotion_hub", "*ดูการประชาสัมพันธ์ของหน่วยตนเองได้"),
            ("create_promotion_hub", "*สร้างการประชาสัมพันธ์ได้"),
            ("edit_promotion_hub", "*แก้ไขการประชาสัมพันธ์ได้"),
            ("delete_promotion_hub", "*ลบการประชาสัมพันธ์ได้"),
            ("detail_promotion_hub", "*ดูรายละเอียดการประชาสัมพันธ์ได้"),

            ("publish_promotion_hub", "*เผยแพร่การประชาสัมพันธ์ได้"),
            ("publish_promotion_hub_airforce", "*เผยแพร่การประชาสัมพันธ์ทั้งทอ.ได้"),

            ("create_promotion_quiz", "*สร้างแบบทดสอบได้"),
            ("edit_promotion_quiz", "*แก้ไขแบบทดสอบได้"),
            ("delete_promotion_quiz", "*ลบแบบทดสอบได้"),
            ("detail_promotion_quiz", "*ดูรายละเอียดแบบทดสอบได้"),

            ("create_promotion_document", "*สร้างเอกสารได้"),
            ("edit_promotion_document", "*แก้ไขเอกสารได้"),
            ("delete_promotion_document", "*ลบเอกสารได้"),
            ("detail_promotion_document", "*ดูรายละเอียดเอกสารได้"),
        ]

    def __str__(self):
        return self.title

    @property
    def num_accepted(self):
        return PromotionView.objects.filter(
            promotion=self,
            accepted=True
        ).count()


    def send_notify(self, users: list, url: str = ""):
        plain_text = strip_tags(self.content or "")

        send_notification(
            title=self.title,
            message=plain_text,
            user_ids=users,
            url=f'https://safety-analysis.rtaf.mi.th/promotion/detail/{self.id}/',
            using_auth=True
        )


class PromotionView(models.Model):
    user = models.ForeignKey(RTAFUser, verbose_name="ผู้เข้าชม", on_delete=models.SET_NULL, null=True, blank=True)
    promotion = models.ForeignKey(Promotion, verbose_name="โปรโมชั่น", on_delete=models.SET_NULL, null=True, blank=True)
    viewed_at = models.DateTimeField(verbose_name="วันที่เข้าชม", auto_now_add=True)

    accepted = models.BooleanField(verbose_name="รับทราบ", default=False)

    class Meta:
        verbose_name = verbose_name_plural = "2. การเข้าชม"

    def __str__(self):
        return f"{self.user} - {self.promotion}"
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.promotion.num_view += 1
            self.promotion.save()
        super().save(*args, **kwargs)


class PromotionImage(models.Model):
    promotion = models.ForeignKey(Promotion,on_delete=models.CASCADE,related_name="images")
    image = models.ImageField(upload_to="promotion/images/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = "รูปภาพประกอบ"

    def __str__(self):
        return self.image.name


class Document(models.Model):
    title = models.CharField("ชื่อ", max_length=255, blank=True)
    description = models.TextField("คำอธิบาย", blank=True)
    promotion = models.OneToOneField(Promotion, verbose_name="โปรโมชั่น", on_delete=models.CASCADE, related_name="documents", null=True, blank=True)

    user = models.ForeignKey(RTAFUser, verbose_name="ผู้สร้าง", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField("วันที่สร้าง", auto_now_add=True)
    updated_at = models.DateTimeField("วันที่แก้ไข", auto_now=True)

    class Meta:
        verbose_name = verbose_name_plural = "7. เอกสารแจ้งเตือน"

    def __str__(self):
        return f"{self.promotion}"
    


class DocumentFile(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="files", verbose_name="แฟ้มเอกสาร")
    file = models.FileField(verbose_name="ไฟล์",upload_to="promotion/documents/")
    title = models.CharField("ชื่อไฟล์", max_length=255, blank=True)
    description = models.TextField("คำอธิบาย", blank=True)
    order = models.PositiveIntegerField("ลำดับ", default=0)

    user = models.ForeignKey(RTAFUser, verbose_name="ผู้สร้าง", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField("วันที่เพิ่ม", auto_now_add=True)
    updated_at = models.DateTimeField("วันที่แก้ไข", auto_now=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = verbose_name_plural = "7.5 ไฟล์ - เอกสารแจ้งเตือน"

    def __str__(self):
        return self.title or self.file.name

    @property
    def file_type(self):
        """คืน type เช่น pdf, image, video"""
        type_, _ = mimetypes.guess_type(self.file.url)
        if not type_:
            return "other"
        return type_.split("/")[0] 

