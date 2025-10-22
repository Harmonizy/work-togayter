from django.contrib import admin
from .models import Promotion, PromotionView, Quiz, Question, Choice, QuizResult


# --- Choice inline (สำหรับ QuestionAdmin) ---
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2
    min_num = 1


# --- Question inline (สำหรับ QuizAdmin) ---
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    show_change_link = True


# --- Quiz Admin ---
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "question_count")
    search_fields = ("title", "description")
    inlines = [QuestionInline]

    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = "จำนวนคำถาม"


# --- Question Admin (แสดง Choice inline ด้านใน) ---
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("quiz", "short_question_text", "choice_count")
    search_fields = ("question_text",)
    inlines = [ChoiceInline]

    def choice_count(self, obj):
        return obj.choices.count()
    choice_count.short_description = "จำนวนตัวเลือก"

    def short_question_text(self, obj):
        return (obj.question_text[:70] + "...") if len(obj.question_text) > 70 else obj.question_text
    short_question_text.short_description = "คำถาม"


# --- Promotion Admin ---
@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "publish", "user", "created_at", "updated_at")
    list_filter = ("status", "publish", "created_at")
    search_fields = ("title", "content")
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("user", "quiz")
    date_hierarchy = "created_at"

    fieldsets = (
        (None, {"fields": ("image", "title", "content")}),
        ("สถานะและการเผยแพร่", {"fields": ("status", "publish")}),
        ("ข้อมูลอื่น ๆ", {"fields": ("quiz", "user", "created_at", "updated_at")}),
    )


# --- Promotion View (ผู้เข้าชม) ---
@admin.register(PromotionView)
class PromotionViewAdmin(admin.ModelAdmin):
    list_display = ("promotion", "user", "viewed_at")
    list_filter = ("viewed_at",)
    search_fields = ("promotion__title", "user__username")


# --- Quiz Result (ผลการทำแบบทดสอบ) ---
@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ("quiz", "user", "score", "completed_at")
    list_filter = ("quiz", "completed_at")
    search_fields = ("user__username", "quiz__title")
    readonly_fields = ("completed_at",)
