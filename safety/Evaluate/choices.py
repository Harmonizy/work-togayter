from django.db import models


class EvaluationAnswerChoices(models.TextChoices):
    YES = 'y', 'ใช่'
    NO = 'n', 'ไม่ใช่'