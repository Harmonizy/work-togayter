from django.db import models

from .choices import EvaluationAnswerChoices
from safety.Report.models import BaseReport
from common.RTAFUser.models import RTAFUser

class ResultType(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    serious_level = models.IntegerField(verbose_name="ระดับความรุนแรง", default=0, help_text="ระดับ 1 - 5 ค่าตัวเลขยิ่งมาก ยิ่งรุนแรง")
    name = models.CharField(max_length=60)
    english_name = models.CharField(max_length=30)
    
    class Meta:
        verbose_name = verbose_name_plural = "ประเภทผลการประเมิน"
        
    def __str__(self):
        return self.name


class EvaluationResult(models.Model):
    type = models.ForeignKey(ResultType, to_field='code', related_name='evaluation_results', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=120)
    english_name = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name =  verbose_name_plural = "1. รายการผลการประเมิน"
    def __str__(self):
        return self.name


class QuestionSet(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    start_question = models.ForeignKey('EvaluationQuestion', null=True, blank=True, related_name='start_of_sets', on_delete=models.SET_NULL)

    class Meta:
        verbose_name =  verbose_name_plural = "2. ชุดคำถาม"

    def __str__(self):
        return self.name
    

class EvaluationQuestion(models.Model):
    question_set = models.ForeignKey(QuestionSet, related_name='questions', on_delete=models.CASCADE, null=True, blank=True)
    text = models.CharField(verbose_name="คำถามประเมิน", max_length=256)

    next_if_yes = models.ForeignKey('self', null=True, blank=True, related_name='prev_yes', on_delete=models.SET_NULL)
    next_if_no = models.ForeignKey('self', null=True, blank=True, related_name='prev_no', on_delete=models.SET_NULL)

    result_if_yes = models.ForeignKey(EvaluationResult, null=True, blank=True, related_name='questions_yes', on_delete=models.SET_NULL)
    result_if_no = models.ForeignKey(EvaluationResult, null=True, blank=True, related_name='questions_no', on_delete=models.SET_NULL)

    class Meta:
        verbose_name = verbose_name_plural = "3. คำถามประเมิน"
    def __str__(self):
        return self.text


class BaseReportEvaluation(models.Model):
    report = models.ForeignKey(BaseReport, on_delete=models.CASCADE, related_name='evaluation')
    question_set = models.ForeignKey(QuestionSet, related_name='evaluations', on_delete=models.CASCADE, null=True, blank=True)
    final_result = models.ForeignKey(EvaluationResult, null=True, blank=True, related_name='evaluations', on_delete=models.SET_NULL)
    
    evaluator = models.ForeignKey(RTAFUser, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="ผู้ประเมิน")
    evaluated_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่ประเมิน", null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = "4. การประเมินผล Report"
        indexes = [
            models.Index(fields=['report', 'question_set', 'evaluator']),
            models.Index(fields=['-evaluated_at']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['report', 'question_set', 'evaluator'],
                name='uniq_report_qset_evaluator',
                nulls_distinct=False,
            ),
        ]
    def __str__(self):
        return f"Evaluation for {self.report}"


class EvaluationAnswer(models.Model):
    order = models.PositiveIntegerField(verbose_name="ลำดับ", default=0)
    evaluation = models.ForeignKey(BaseReportEvaluation, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(EvaluationQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1, choices=EvaluationAnswerChoices.choices, default=EvaluationAnswerChoices.NO)

    class Meta:
        verbose_name = verbose_name_plural = "คำตอบ"
        ordering = ['evaluation', 'order']
        
    def __str__(self):
        return f"{self.question} => {self.get_answer_display()}"
    
    def save(self, *args, **kwargs):
        if self.order == 0:
            last_order = EvaluationAnswer.objects.filter(evaluation=self.evaluation).aggregate(models.Max('order'))['order__max']
            self.order = (last_order or 0) + 1
        super().save(*args, **kwargs)
