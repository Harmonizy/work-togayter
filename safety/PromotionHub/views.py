from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from django.contrib import messages

from .models import Promotion, PromotionView, Quiz, Question, Choice, QuizResult
from .forms import PromotionForm



def list(request):
    promotions = Promotion.objects.all
    context = {
        "promotions": promotions
    }
    return render(request, "PromotionHub/promotion_list.html", context)


@login_required
def detail(request, pk):
    promotion = get_object_or_404(Promotion, pk=pk)

    PromotionView.objects.create(
        user=request.user,
        promotion=promotion,
        viewed_at=timezone.now()
    )

    view_count = PromotionView.objects.filter(promotion=promotion).count()

    context = {
        "promotion": promotion,
        "view_count": view_count
    }
    return render(request, "PromotionHub/promotion_detail.html", context)


@login_required
def create(request):
    if request.method == "POST":
        form = PromotionForm(request.POST, request.FILES)
        if form.is_valid():
            promotion = form.save(commit=False)
            promotion.user = request.user
            promotion.save()
            messages.success(request, "สร้างบทความใหม่เรียบร้อยแล้ว!")
            return redirect("promotion:list")
        else:
            messages.error(request, "ไม่สามารถบันทึกได้ กรุณาตรวจสอบข้อมูลอีกครั้ง")
    else:
        form = PromotionForm()

    context = {
        "form": form,
    }
    return render(request, "PromotionHub/promotion_create.html", context)


@login_required
def edit(request, pk):
    promotion = get_object_or_404(Promotion, pk=pk)

    if request.method == "POST":
        form = PromotionForm(request.POST, request.FILES, instance=promotion)
        if form.is_valid():
            form.save()
            messages.success(request, "แก้ไขบทความเรียบร้อยแล้ว!")
            return redirect("promotion:detail", pk=promotion.pk)
        else:
            messages.error(request, "ไม่สามารถบันทึกได้ กรุณาตรวจสอบข้อมูลอีกครั้ง")
    else:
        form = PromotionForm(instance=promotion)

    context = {
        "form": form,
        "promotion": promotion,
    }
    return render(request, "PromotionHub/promotion_edit.html", context)


@login_required
def delete(request, pk):
    promotion = get_object_or_404(Promotion, pk=pk)
    promotion.delete()
    messages.success(request, "ลบบทความเรียบร้อยแล้ว!")
    return redirect("promotion:list")


@login_required
def quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.prefetch_related('choices').all()

    if request.method == "POST":
        score = 0
        total = questions.count()

        for question in questions:
            selected_choice_id = request.POST.get(str(question.id))
            if selected_choice_id:
                choice = Choice.objects.filter(id=selected_choice_id, question=question).first()
                if choice and choice.is_correct:
                    score += 1

        result = QuizResult.objects.create(
            quiz=quiz,
            user=request.user,
            score=(score / total) * 100 if total > 0 else 0
        )

        messages.success(request, f"คุณได้คะแนน {result.score:.0f}%")
        return redirect("safety_promotion:quiz_result", result.id)

    context = {
        "quiz": quiz,
        "questions": questions,
    }
    return render(request, "PromotionHub/quiz.html", context)


@login_required
def quiz_result(request, result_id):
    result = get_object_or_404(QuizResult, id=result_id, user=request.user)

    context = {
        "result": result,
        "quiz": result.quiz,
    }
    return render(request, "PromotionHub/quiz_result.html", context)
