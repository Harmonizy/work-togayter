from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count, Q
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.http import JsonResponse
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.paginator import Paginator

from .models import Promotion, PromotionView, Quiz, Question, Choice, QuizResult, Document, DocumentFile
from .forms import PromotionForm, QuizForm, QuestionFormSet, ChoiceFormSet, DocumentForm, DocumentFileForm
from .choices import PromotionStatusChoices, PromotionPublishChoices, PromotionPriorityChoices, PromotionTypeChoices
from common.RTAFAuth.views import SuperAppLoginMixins
from common.RTAFUser.models import RTAFUser, Affiliation


@login_required
def list_ground(request):
    user = request.user

    # Superuser เห็นหมด (เฉพาะ GROUND)
    if user.is_superuser or user.has_perm("PromotionHub.view_all_promotion_hub"):
        promotions = Promotion.objects.filter(type=PromotionTypeChoices.GROUND,priority=PromotionPriorityChoices.NONE)

    # เห็นเฉพาะของหน่วยตัวเอง (เฉพาะ GROUND)
    elif user.has_perm("PromotionHub.view_affiliation_promotion_hub"):
        promotions = Promotion.objects.filter(
            user__affiliation=user.affiliation,
            type=PromotionTypeChoices.GROUND,
            priority=PromotionPriorityChoices.NONE
        )

    else:
        promotions = Promotion.objects.none()

    # เฉพาะที่เผยแพร่แล้ว
    published = Promotion.objects.filter(
        status=PromotionStatusChoices.PUBLISHED,
        type=PromotionTypeChoices.GROUND,
        priority=PromotionPriorityChoices.NONE
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

    context = {
        "promotions": promotions,
        "type": "ภาคพื้น"
    }
    return render(request, "PromotionHub/promotion_list.html", context)


@login_required
def list_air(request):
    user = request.user

    # Superuser เห็นหมด (เฉพาะ AIR)
    if user.is_superuser or user.has_perm("PromotionHub.view_all_promotion_hub"):
        promotions = Promotion.objects.filter(type=PromotionTypeChoices.AIR, priority=PromotionPriorityChoices.NONE)

    # เห็นเฉพาะของหน่วยตัวเอง (เฉพาะ AIR)
    elif user.has_perm("PromotionHub.view_affiliation_promotion_hub"):
        promotions = Promotion.objects.filter(
            user__affiliation=user.affiliation,
            type=PromotionTypeChoices.AIR,
            priority=PromotionPriorityChoices.NONE
        )

    else:
        promotions = Promotion.objects.none()

    # เฉพาะที่เผยแพร่แล้ว
    published = Promotion.objects.filter(
        status=PromotionStatusChoices.PUBLISHED,
        type=PromotionTypeChoices.AIR,
        priority=PromotionPriorityChoices.NONE
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

    context = {
        "promotions": promotions,
        "type": "การบิน"
    }
    return render(request, "PromotionHub/promotion_list.html", context)


@login_required
def announcement_list(request):
    user = request.user

    # Superuser เห็นหมด (เฉพาะ GROUND)
    if user.is_superuser or user.has_perm("PromotionHub.view_all_promotion_hub"):
        promotions = Promotion.objects.filter(priority=PromotionPriorityChoices.HIGH)

    # เห็นเฉพาะของหน่วยตัวเอง (เฉพาะ GROUND)
    elif user.has_perm("PromotionHub.view_affiliation_promotion_hub"):
        promotions = Promotion.objects.filter(
            user__affiliation=user.affiliation,
            priority=PromotionPriorityChoices.HIGH
        )

    else:
        promotions = Promotion.objects.none()

    # เฉพาะที่เผยแพร่แล้ว
    published = Promotion.objects.filter(
        status=PromotionStatusChoices.PUBLISHED,
        priority=PromotionPriorityChoices.HIGH
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

    context = {
        "promotions": promotions,
        "type": "การแจ้งเตือน"
    }
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

        promotion_view, created = PromotionView.objects.get_or_create(
            user=self.request.user,
            promotion=promotion,
            defaults={'viewed_at': timezone.now()}
        )

        context['promotion_view'] = promotion_view
        context['view_count'] = PromotionView.objects.filter(promotion=promotion).count()

        quiz = promotion.quiz
        if quiz:
            context["quiz"] = quiz
            context["quiz_completed_count"] = quiz.num_completed

            user_done = QuizResult.objects.filter(
                quiz=quiz,
                user=self.request.user
            ).exists()
            context["user_completed_quiz"] = user_done
        else:
            context["quiz"] = None

        return context


@login_required
def create_ground(request):
    if request.method == "POST":
        form = PromotionForm(request.POST, request.FILES)
        if form.is_valid():
            promotion = form.save(commit=False)
            promotion.user = request.user
            promotion.priority = PromotionPriorityChoices.NONE
            promotion.type = PromotionTypeChoices.GROUND
            promotion.save()
            messages.success(request, "สร้างบทความใหม่เรียบร้อยแล้ว!")
            return redirect("promotion:list_ground")
        else:
            messages.error(request, "ไม่สามารถบันทึกได้ กรุณาตรวจสอบข้อมูลอีกครั้ง")
    else:
        form = PromotionForm()

    context = {
        "form": form,
        "type" : "ภาคพื้น"
    }
    return render(request, "PromotionHub/promotion_create.html", context)


@login_required
def create_air(request):
    if request.method == "POST":
        form = PromotionForm(request.POST, request.FILES)
        if form.is_valid():
            promotion = form.save(commit=False)
            promotion.user = request.user
            promotion.priority = PromotionPriorityChoices.NONE
            promotion.type = PromotionTypeChoices.AIR
            promotion.save()
            messages.success(request, "สร้างบทความใหม่เรียบร้อยแล้ว!")
            return redirect("promotion:list_air")
        else:
            messages.error(request, "ไม่สามารถบันทึกได้ กรุณาตรวจสอบข้อมูลอีกครั้ง")
    else:
        form = PromotionForm()

    context = {
        "form": form,
        "type" : "การบิน"
    }
    return render(request, "PromotionHub/promotion_create.html", context)


@login_required
def announcement_create(request):
    if request.method == "POST":
        form = PromotionForm(request.POST, request.FILES)
        if form.is_valid():
            promotion = form.save(commit=False)
            promotion.user = request.user
            promotion.priority = PromotionPriorityChoices.HIGH
            promotion.type = PromotionTypeChoices.NONE
            promotion.save()
            messages.success(request, "สร้างบทความใหม่เรียบร้อยแล้ว!")
            return redirect("promotion:announcement_list")
        else:
            messages.error(request, "ไม่สามารถบันทึกได้ กรุณาตรวจสอบข้อมูลอีกครั้ง")
    else:
        form = PromotionForm()

    context = {
        "form": form,
        "type" : "การแจ้งเตือน"
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

    publish_type = request.POST.get("publish_type")
    users = []

    if publish_type == "A":  # AIRFORCE
        users = RTAFUser.objects.values_list("username", flat=True)

    elif publish_type == "U":  # UNIT
        users = RTAFUser.objects.filter(
            affiliation=promotion.user.affiliation
        ).values_list("username", flat=True)

    elif publish_type == "G":  # GROUP
        group_ids = request.POST.getlist("groups")
        users = RTAFUser.objects.filter(
            groups__id__in=group_ids
        ).distinct().values_list("username", flat=True)

    promotion.status = PromotionStatusChoices.PUBLISHED
    promotion.publish = publish_type
    promotion.save()

    promotion.send_notify(list(users))

    return HttpResponse("<p class='text-success'>เผยแพร่เรียบร้อยแล้ว</p>")


def quiz_list(request):
    quizzes = Quiz.objects.all().order_by('-id')
    return render(request, 'PromotionHub/quiz_list.html', {'quizzes': quizzes})


def quiz_create(request):

    # ใช้ prefix มาตรฐาน
    q_prefix = "questions"

    if request.method == "POST":
        quiz_form = QuizForm(request.POST)
        question_formset = QuestionFormSet(request.POST, prefix=q_prefix)

        if quiz_form.is_valid() and question_formset.is_valid():
            quiz = quiz_form.save()

            for q_index, q_form in enumerate(question_formset):
                question = q_form.save(commit=False)
                question.quiz = quiz
                question.save()

                choice_formset = ChoiceFormSet(
                    request.POST,
                    prefix=f"choice_{q_index}",
                    instance=question
                )

                if choice_formset.is_valid():
                    choice_formset.save()

            return redirect("promotion:quiz_list")

    else:
        quiz_form = QuizForm()
        question_formset = QuestionFormSet(prefix=q_prefix)

    # --------------------------------------------
    # empty form สำหรับ JS clone
    # --------------------------------------------

    # empty question form
    q_empty = QuestionFormSet(prefix=q_prefix).empty_form.as_p()
    q_empty = q_empty.replace(f"{q_prefix}-__prefix__", f"{q_prefix}-__qindex__")

    # empty choice form
    c_empty = ChoiceFormSet(prefix="choice_EMPTY").empty_form.as_p()
    c_empty = c_empty.replace("choice_EMPTY-__prefix__", "choice___qindex__-__cindex__")

    # empty choice management_form
    c_mgmt = ChoiceFormSet(prefix="choice_EMPTY").management_form.as_p()
    c_mgmt = c_mgmt.replace("choice_EMPTY", "choice___qindex__")

    # --------------------------------------------

    choice_formsets = [
        ChoiceFormSet(prefix=f"choice_{i}")
        for i in range(question_formset.total_form_count())
    ]

    question_and_choices = zip(question_formset, choice_formsets)

    return render(request, "PromotionHub/quiz_create.html", {
        "quiz_form": quiz_form,
        "question_formset": question_formset,
        "question_and_choices": question_and_choices,

        "empty_question_html": q_empty,
        "empty_choice_html": c_empty,
        "empty_choice_mgmt": c_mgmt,
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


def quiz_result_modal(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    results = QuizResult.objects.filter(quiz_id=quiz_id).select_related("user")
    return render(request, "PromotionHub/Quiz/components/quiz_result_modal.html", {
        "quiz": quiz,
        "results": results
    })


@login_required
@permission_required("PromotionHub.publish_promotion_hub", raise_exception=True)
def publish_modal(request, pk):
    promotion = get_object_or_404(Promotion, pk=pk)
    affiliations = Affiliation.objects.all()
    groups = Group.objects.all()

    return render(request, "PromotionHub/Promotion/components/publish_modal.html", {
        "promotion": promotion,
        "groups": groups,
        "affiliations": affiliations
    })
    

@login_required
def publish_dynamic_options(request, pk):
    promotion = get_object_or_404(Promotion, pk=pk)
    publish_type = request.GET.get("publish_type")

    groups = Group.objects.all()

    return render(request, "PromotionHub/Promotion/components/publish_dynamic_options.html", {
        "publish_type": publish_type,
        "groups": groups
    })


@login_required
def document_list(request):
    search = request.GET.get("search", "").strip()

    documents = Document.objects.all()

    if search:
        documents = documents.filter(
            Q(title__icontains=search) |
            Q(promotion__title__icontains=search)
        )

    documents = documents.order_by("-created_at")

    context = {
        "documents": documents,
        "search": search,
    }
    return render(request, "PromotionHub/Document/document_list.html", context)


@login_required
def document_detail(request, pk):
    document = get_object_or_404(Document, pk=pk)

    context = {
        "document": document,
        "files": document.files.all()
    }
    return render(request, "PromotionHub/Document/document_detail.html", context)


@login_required
def document_create(request):
    if request.method == "POST":
        form = DocumentForm(request.POST)

        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user     # ตั้งค่าเจ้าของ
            document.save()

            # หากต้อง redirect ไปหน้า detail ของ promotion
            if document.promotion:
                return redirect("promotion:detail", pk=document.promotion.id)

            return redirect("document:list")  # หรือจะ redirect ที่อื่นก็ได้

    else:
        form = DocumentForm()

    return render(request, "PromotionHub/Document/document_form.html", {
        "form": form
    })


@login_required
def document_edit(request, pk):
    document = get_object_or_404(Document, pk=pk)

    if request.method == "POST":
        form = DocumentForm(request.POST, instance=document)

        if form.is_valid():
            doc = form.save(commit=False)
            doc.user = request.user  # อัปเดตผู้แก้ไขคนล่าสุดก็ได้
            doc.save()

            # หากต้อง redirect ไป promotion detail
            if doc.promotion:
                return redirect("promotion:detail", pk=doc.promotion.id)

            return redirect("document:list")
    else:
        form = DocumentForm(instance=document)

    return render(request, "PromotionHub/Document/document_form.html", {
        "form": form,
        "document": document
    })


@login_required
def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk)
    document.delete()
    messages.success(request, "ลบเอกสารสำเร็จ")
    return redirect("promotion:document_list")


@login_required
def document_add_file(request, pk):
    document = get_object_or_404(Document, pk=pk)

    if request.method == "POST":
        form = DocumentFileForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.document = document
            obj.user = request.user
            obj.save()
            response = HttpResponse("")
            response["HX-Redirect"] = reverse("promotion:document_detail", args=[pk])
            return response

    form = DocumentFileForm()
    return render(request, "PromotionHub/Document/document_add_file.html", {
        "form": form,
        "document": document,
    })


@login_required
def document_file_list(request, pk):
    document = get_object_or_404(Document, pk=pk)

    page = request.GET.get("page", 1)

    paginator = Paginator(document.files.all(), 5)
    page_obj = paginator.get_page(page)

    return render(
        request,
        "PromotionHub/Document/components/file_list.html",
        {"document": document, "page_obj": page_obj},
    )
    

@login_required
def document_file_delete(request, file_id):
    if request.method == "POST":
        file_obj = get_object_or_404(DocumentFile, id=file_id)
        doc_pk = file_obj.document.pk
        file_obj.delete()
        return document_file_list(request, doc_pk)

    return HttpResponseBadRequest("Invalid request")