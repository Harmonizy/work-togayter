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
@permission_required("PromotionHub.edit_promotion_hub", raise_exception=True)
def edit(request, pk):
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