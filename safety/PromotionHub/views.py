from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView


from .models import Promotion, PromotionView, Quiz, Question, Choice, QuizResult
from .forms import PromotionForm
from .choices import PromotionStatusChoices, PromotionPublishChoices
from common.RTAFAuth.views import SuperAppLoginMixins
from common.RTAFUser.models import RTAFUser


@login_required
def list(request):
    user = request.user

    # Superuser เห็นหมด
    if user.is_superuser or user.has_perm("PromotionHub.view_all_promotion_hub"):
        promotions = Promotion.objects.all()

    # เห็นเฉพาะของหน่วยตัวเอง
    elif user.has_perm("PromotionHub.view_affiliation_promotion_hub"):
        promotions = Promotion.objects.filter(
            user__affiliation=user.affiliation
        )

    else:
        raise PermissionDenied("คุณไม่มีสิทธิ์ดูรายการประชาสัมพันธ์")

    # เพิ่มการกรองเฉพาะที่เผยแพร่แล้ว
    published = Promotion.objects.filter(
        status=PromotionStatusChoices.PUBLISHED
    )

    # รวมกับ logic การเผยแพร่ (หน่วย / ทอ.)
    visible_promotions = published.filter(
        publish=PromotionPublishChoices.AIRFORCE
    ) | published.filter(
        publish=PromotionPublishChoices.UNIT, user__affiliation=user.affiliation
    )

    # รวมทั้งหมดแล้วลบซ้ำ
    promotions = (promotions | visible_promotions).distinct().order_by("-created_at")

    context = {"promotions": promotions}
    return render(request, "PromotionHub/promotion_list.html", context)


# @login_required
def detail(request, pk):
    promotion = get_object_or_404(Promotion, pk=pk)

    already_viewed = PromotionView.objects.filter(
        user=request.user,
        promotion=promotion
    ).exists()

    if not already_viewed:
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


class PromotionDetailView(LoginRequiredMixin, SuperAppLoginMixins, DetailView):
    model = Promotion
    template_name = 'PromotionHub/promotion_detail.html'
    context_object_name = 'promotion'

    def get_success_url(self):
        return self.request.get_full_path().split('?')[0]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        view_count = PromotionView.objects.filter(promotion=self.get_object()).count()
        context['view_count'] = view_count
        return context
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if request.user.is_authenticated:
            PromotionView.objects.update_or_create(
                user=request.user,
                promotion=self.get_object(),
                defaults={'viewed_at': timezone.now()}
            )
        return response


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
    user = request.user

    # ตรวจสิทธิ์
    if not (user.is_superuser or user.has_perm("PromotionHub.edit_promotion_hub") or promotion.user == user):
        raise PermissionDenied("คุณไม่มีสิทธิ์แก้ไขบทความนี้")

    if request.method == "POST":
        form = PromotionForm(request.POST, request.FILES, instance=promotion)
        if form.is_valid():
            form.save()
            messages.success(request, "แก้ไขบทความเรียบร้อยแล้ว!")
            return redirect("promotion:detail", pk=promotion.pk)
    else:
        form = PromotionForm(instance=promotion)

    return render(request, "PromotionHub/promotion_edit.html", {"form": form, "promotion": promotion})


@login_required
def delete(request, pk):
    promotion = get_object_or_404(Promotion, pk=pk)
    user = request.user

    if not (user.is_superuser or user.has_perm("PromotionHub.delete_promotion_hub") or promotion.user == user):
        raise PermissionDenied("คุณไม่มีสิทธิ์ลบบทความนี้")

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
        return redirect("promotion:quiz_result", result.id)

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


@login_required
@permission_required("PromotionHub.publish_promotion_hub", raise_exception=True)
def publish_promotion(request, pk):
    promotion = get_object_or_404(Promotion, pk=pk)

    if promotion.publish == PromotionPublishChoices.AIRFORCE:
        users = RTAFUser.objects.values_list("username", flat=True)

    elif promotion.publish == PromotionPublishChoices.UNIT:
        users = RTAFUser.objects.filter(
            affiliation=promotion.user.affiliation
        ).values_list("username", flat=True)

    else:
        users = []

    promotion.send_notify(list(users))

    messages.success(request, "✅ เผยแพร่ประชาสัมพันธ์เรียบร้อย และส่งการแจ้งเตือนแล้ว.")
    return redirect("PromotionHub:promotion.detail", pk=promotion.id)