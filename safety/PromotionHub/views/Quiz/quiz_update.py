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


def update(request, id):
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