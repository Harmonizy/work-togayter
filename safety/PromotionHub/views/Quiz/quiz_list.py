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

@login_required
def list(request):
    quizzes = Quiz.objects.all().order_by('-id')
    return render(request, 'PromotionHub/quiz_list.html', {'quizzes': quizzes})


def result_modal(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    results = QuizResult.objects.filter(quiz_id=quiz_id).select_related("user")
    return render(request, "PromotionHub/Quiz/components/quiz_result_modal.html", {
        "quiz": quiz,
        "results": results
    })