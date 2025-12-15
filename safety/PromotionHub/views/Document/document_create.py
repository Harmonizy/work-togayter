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
@permission_required("PromotionHub.create_promotion_document", raise_exception=True)
def create(request):
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