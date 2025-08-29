from django.contrib import admin
from django.db import models
from django import forms

from .models import (
    ResultType,
    EvaluationResult,
    QuestionSet,
    EvaluationQuestion,
    BaseReportEvaluation,
    EvaluationAnswer
)

@admin.register(ResultType)
class ResultTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'english_name', 'serious_level')
    search_fields = ('name', 'english_name')

@admin.register(EvaluationResult)
class EvaluationResultAdmin(admin.ModelAdmin):
    list_display = ('type', 'name', 'english_name', 'description')
    list_display_links = ('name', 'english_name')
    search_fields = ('name',)
    list_filter = ('type',)


class EvaluationQuestionInline(admin.TabularInline):
    model = EvaluationQuestion
    extra = 0
    autocomplete_fields = ['next_if_yes', 'next_if_no', 'result_if_yes', 'result_if_no']



@admin.register(EvaluationQuestion)
class EvaluationQuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question_set')
    search_fields = ('text',)
    autocomplete_fields = ['next_if_yes', 'next_if_no', 'result_if_yes', 'result_if_no']


@admin.register(QuestionSet)
class QuestionSetAdmin(admin.ModelAdmin):
    list_display = ('name',) # 'next_if_yes', 'next_if_no', 'result_if_yes', 'result_if_no')
    search_fields = ('name',)
    inlines = [EvaluationQuestionInline]
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'cols': 40})},
    }


class EvaluationAnswerInline(admin.TabularInline):
    model = EvaluationAnswer
    extra = 0
    readonly_fields = ('order',)
    fields = ('order', 'question', 'answer')
    # autocomplete_fields = ['question']
    can_delete = False
    show_change_link = True


@admin.register(BaseReportEvaluation)
class BaseReportEvaluationAdmin(admin.ModelAdmin):
    list_display = ('report', 'question_set', 'final_result')
    search_fields = ('report__title',)
    # autocomplete_fields = ['report', 'current_question', 'final_result']
    inlines = [EvaluationAnswerInline]
