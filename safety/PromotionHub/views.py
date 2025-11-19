from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.http import JsonResponse


from .models import Promotion, PromotionView, Quiz, Question, Choice, QuizResult
from .forms import PromotionForm, QuizForm, QuestionFormSet, ChoiceFormSet
from .choices import PromotionStatusChoices, PromotionPublishChoices, PromotionPriorityChoices, PromotionTypeChoices
from common.RTAFAuth.views import SuperAppLoginMixins
from common.RTAFUser.models import RTAFUser, Affiliation


@login_required
def list_ground(request):
    user = request.user

    # Superuser เห็นหมด (เฉพาะ GROUND)
    if user.is_superuser or user.has_perm("PromotionHub.view_all_promotion_hub"):
        promotions = Promotion.objects.filter(type=PromotionTypeChoices.GROUND)

    # เห็นเฉพาะของหน่วยตัวเอง (เฉพาะ GROUND)
    elif user.has_perm("PromotionHub.view_affiliation_promotion_hub"):
        promotions = Promotion.objects.filter(
            user__affiliation=user.affiliation,
            type=PromotionTypeChoices.GROUND
        )

    else:
        raise PermissionDenied("คุณไม่มีสิทธิ์ดูรายการประชาสัมพันธ์")

    # เฉพาะที่เผยแพร่แล้ว
    published = Promotion.objects.filter(
        status=PromotionStatusChoices.PUBLISHED,
        type=PromotionTypeChoices.GROUND
    )

    # เผยแพร่ระดับ ทอ. หรือเฉพาะหน่วย
    visible_promotions = (
        published.filter(publish=PromotionPublishChoices.AIRFORCE)
        |
        published.filter(
            publish=PromotionPublishChoices.UNIT,
            user__affiliation=user.affiliation
        )
    )

    # รวม + distinct + sort
    promotions = (promotions | visible_promotions).distinct().order_by("-created_at")

    context = {"promotions": promotions}
    return render(request, "PromotionHub/promotion_list.html", context)


@login_required
def list_air(request):
    user = request.user

    # Superuser เห็นหมด (เฉพาะ AIR)
    if user.is_superuser or user.has_perm("PromotionHub.view_all_promotion_hub"):
        promotions = Promotion.objects.filter(type=PromotionTypeChoices.AIR)

    # เห็นเฉพาะของหน่วยตัวเอง (เฉพาะ AIR)
    elif user.has_perm("PromotionHub.view_affiliation_promotion_hub"):
        promotions = Promotion.objects.filter(
            user__affiliation=user.affiliation,
            type=PromotionTypeChoices.AIR
        )

    else:
        raise PermissionDenied("คุณไม่มีสิทธิ์ดูรายการประชาสัมพันธ์")

    # เฉพาะที่เผยแพร่แล้ว
    published = Promotion.objects.filter(
        status=PromotionStatusChoices.PUBLISHED,
        type=PromotionTypeChoices.AIR
    )

    # เผยแพร่ระดับ ทอ. หรือเฉพาะหน่วย
    visible_promotions = (
        published.filter(publish=PromotionPublishChoices.AIRFORCE)
        |
        published.filter(
            publish=PromotionPublishChoices.UNIT,
            user__affiliation=user.affiliation
        )
    )

    # รวม + distinct + sort
    promotions = (promotions | visible_promotions).distinct().order_by("-created_at")

    context = {"promotions": promotions}
    return render(request, "PromotionHub/promotion_list.html", context)


# @login_required
# def detail(request, pk):
#     promotion = get_object_or_404(Promotion, pk=pk)

#     # ต้องแยกออกเป็นสองตัวแปร ไม่ใช่ตัวเดียว
#     promotion_view, created = PromotionView.objects.get_or_create(
#         user=request.user,
#         promotion=promotion,
#         defaults={'viewed_at': timezone.now()}
#     )

#     view_count = PromotionView.objects.filter(promotion=promotion).count()

#     context = {
#         "promotion": promotion,
#         "promotion_view": promotion_view,  # <- ตอนนี้เป็น instance จริง
#         "view_count": view_count,
#     }
#     return render(request, "PromotionHub/promotion_detail.html", context)


class PromotionDetailView(LoginRequiredMixin, SuperAppLoginMixins, DetailView):
    model = Promotion
    template_name = 'PromotionHub/promotion_detail.html'
    context_object_name = 'promotion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        promotion = self.get_object()

        # ⭐ ดึง PromotionView ให้แน่นอน
        promotion_view, created = PromotionView.objects.get_or_create(
            user=self.request.user,
            promotion=promotion,
            defaults={'viewed_at': timezone.now()}
        )

        context['promotion_view'] = promotion_view
        context['view_count'] = PromotionView.objects.filter(promotion=promotion).count()
        return context
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        # ⭐ นับ view เฉพาะตอนแรกที่สร้างเท่านั้น (ตาม save() ของคุณ)
        if request.user.is_authenticated:
            PromotionView.objects.get_or_create(
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


def quiz_list(request):
    quizzes = Quiz.objects.all().order_by('-id')
    return render(request, 'PromotionHub/quiz_list.html', {'quizzes': quizzes})


def quiz_create(request):
    if request.method == "POST":
        quiz_form = QuizForm(request.POST)
        question_formset = QuestionFormSet(request.POST)

        choice_formsets = []

        if quiz_form.is_valid() and question_formset.is_valid():
            quiz = quiz_form.save()
            questions = question_formset.save(commit=False)

            for index, q in enumerate(questions):
                q.quiz = quiz
                q.save()

                # สร้าง ChoiceFormSet สำหรับคำถามแต่ละข้อ
                choice_formset = ChoiceFormSet(
                    request.POST,
                    instance=q,
                    prefix=f"choice_{index}"
                )

                if choice_formset.is_valid():
                    choice_formset.save()
                else:
                    print("Choice error:", choice_formset.errors)

            return redirect("promotion:quiz_list")

    else:
        quiz_form = QuizForm()
        question_formset = QuestionFormSet()

        # choice formsets ตามจำนวน question form
        choice_formsets = [
            ChoiceFormSet(prefix=f"choice_{i}")
            for i, _ in enumerate(question_formset)
        ]

    # ⬅⬅⬅ สำคัญ! รวมคู่ Question + ChoiceFormSets
    question_and_choices = zip(question_formset, choice_formsets)

    return render(request, "PromotionHub/quiz_create.html", {
        "quiz_form": quiz_form,
        "question_formset": question_formset,
        "choice_formsets": choice_formsets,
        "question_and_choices": question_and_choices,  # ⬅ ส่งเข้าหน้า HTML
    })


def quiz_detail(request, id):
    quiz = get_object_or_404(Quiz, id=id)
    questions = quiz.questions.all().prefetch_related('choices')

    return render(request, "PromotionHub/quiz_detail.html", {
        'quiz': quiz,
        'questions': questions
    })


def quiz_update(request, id):
    quiz = get_object_or_404(Quiz, id=id)

    if request.method == "POST":
        quiz_form = QuizForm(request.POST, instance=quiz)
        formset = QuestionFormSet(request.POST, instance=quiz)

        if quiz_form.is_valid() and formset.is_valid():
            quiz_form.save()
            formset.save()
            return redirect("promotion:quiz_detail", id=quiz.id)

    else:
        quiz_form = QuizForm(instance=quiz)
        formset = QuestionFormSet(instance=quiz)

    return render(request, "PromotionHub/quiz_update.html", {
        "quiz_form": quiz_form,
        "question_formset": formset,
        "quiz": quiz,
    })


def quiz_delete(request, id):
    quiz = get_object_or_404(Quiz, id=id)
    quiz.delete()
    return redirect('promotion:quiz_list')


@login_required
def accept(request, pk):
    view = get_object_or_404(PromotionView, pk=pk, user=request.user)

    if request.method == "POST":
        view.accepted = True
        view.save()

    return redirect("promotion:detail", pk=view.promotion.pk)



