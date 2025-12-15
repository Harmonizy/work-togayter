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
def add_file(request, pk):
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
def file_list(request, pk):
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
def file_delete(request, file_id):
    if request.method == "POST":
        file_obj = get_object_or_404(DocumentFile, id=file_id)
        doc_pk = file_obj.document.pk
        file_obj.delete()
        return file_list(request, doc_pk)

    return HttpResponseBadRequest("Invalid request")