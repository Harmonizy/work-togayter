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

from ...models import Promotion, PromotionView, Quiz, Question, Choice, QuizResult, Document, DocumentFile
from ...forms import PromotionForm, QuizForm, QuestionFormSet, ChoiceFormSet, DocumentForm, DocumentFileForm
from ...choices import PromotionStatusChoices, PromotionPublishChoices, PromotionPriorityChoices, PromotionTypeChoices
from common.RTAFAuth.views import SuperAppLoginMixins
from common.RTAFUser.models import RTAFUser, Affiliation


def create(request):
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

    q_empty = QuestionFormSet(prefix=q_prefix).empty_form.as_p()
    q_empty = q_empty.replace(f"{q_prefix}-__prefix__", f"{q_prefix}-__qindex__")

    c_empty = ChoiceFormSet(prefix="choice_EMPTY").empty_form.as_p()
    c_empty = c_empty.replace("choice_EMPTY-__prefix__", "choice___qindex__-__cindex__")

    c_mgmt = ChoiceFormSet(prefix="choice_EMPTY").management_form.as_p()
    c_mgmt = c_mgmt.replace("choice_EMPTY", "choice___qindex__")

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