from django.contrib import admin
from safety.Report.models.sixA import Question, SixA, Answer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    min_num = 0
    show_change_link = False
    fields = ("question", "answer", "note")
    readonly_fields = ("question",)

    def has_add_permission(self, request, obj=None):
        # ไม่ให้กดเพิ่มเอง → ระบบจะ generate จากคำถาม
        return False


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("code", "definition", "category")
    search_fields = ("code", "definition", "description", "note")
    list_filter = ("category",)


@admin.register(SixA)
class SixAAdmin(admin.ModelAdmin):
    list_display = ("report", "user", "created_at")
    list_filter = ("created_at",)
    search_fields = (
        "report__title",
        "report__id",
        "user__first_name",
        "user__last_name",
    )
    inlines = [AnswerInline]

    def save_model(self, request, obj, form, change):
        """
        เมื่อสร้าง SixA ใหม่ → generate answer สำหรับคำถามทุกข้ออัตโนมัติ
        """
        super().save_model(request, obj, form, change)

        if not change:
            for q in Question.objects.all():
                Answer.objects.get_or_create(
                    sixA=obj,
                    question=q,
                )