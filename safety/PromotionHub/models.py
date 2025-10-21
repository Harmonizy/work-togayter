from django.db import models
from common.RTAFUser.models.RTAFUser import RTAFUser, Affiliation
from .choices import PromotionStatusChoices, PromotionPublishChoices

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)


class QuizResult(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(RTAFUser, verbose_name="ผู้เข้าชม", on_delete=models.SET_NULL, null=True, blank=True)
    score = models.FloatField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)


class Promotion(models.Model):
    image = models.ImageField(upload_to='safety_promotion/')
    title = models.CharField(max_length=255)
    content = models.TextField()
    status = models.CharField(verbose_name="สถานะ", max_length=1, choices=PromotionStatusChoices.choices, default=PromotionStatusChoices.DRAFT, null=True, blank=True)
    publish = models.CharField(verbose_name="เผยแพร่", max_length=1, choices=PromotionPublishChoices.choices, default=PromotionPublishChoices.AIRFORCE, null=True, blank=True)

    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True, blank=True)

    user = models.ForeignKey(RTAFUser, verbose_name="ผู้สร้าง", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class PromotionView(models.Model):
    user = models.ForeignKey(RTAFUser, verbose_name="ผู้เข้าชม", on_delete=models.SET_NULL, null=True, blank=True)
    promotion = models.ForeignKey(Promotion, verbose_name="โปรโมชั่น", on_delete=models.SET_NULL, null=True, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)


