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

from ...models import Promotion, PromotionView, Quiz, Question, Choice, QuizResult, Document, DocumentFile, PromotionImage, PromotionFile
from ...forms import PromotionForm, QuizForm, QuestionFormSet, ChoiceFormSet, DocumentForm, DocumentFileForm
from ...choices import PromotionStatusChoices, PromotionPublishChoices, PromotionPriorityChoices, PromotionTypeChoices
from common.RTAFAuth.views import SuperAppLoginMixins
from common.RTAFUser.models import RTAFUser, Affiliation


@login_required
def edit(request, pk):
    promotion = get_object_or_404(Promotion, pk=pk)
    user = request.user

    if not (user.is_superuser or user.has_perm("PromotionHub.edit_promotion_hub") or promotion.user == user):
        raise PermissionDenied("คุณไม่มีสิทธิ์แก้ไขบทความนี้")

    if request.method == "POST":
        form = PromotionForm(request.POST, request.FILES, instance=promotion)
        if form.is_valid():
            promotion = form.save()

            for img in request.FILES.getlist("images"):
                PromotionImage.objects.create(
                    promotion=promotion,
                    image=img
                )

            for f in request.FILES.getlist("files"):
                PromotionFile.objects.create(
                    promotion=promotion,
                    file=f
                )

            messages.success(request, "แก้ไขบทความเรียบร้อยแล้ว!")
            return redirect("promotion:detail", pk=promotion.pk)
    else:
        form = PromotionForm(instance=promotion)

    return render(request, "PromotionHub/promotion_edit.html", {
        "form": form,
        "promotion": promotion,
        "images": promotion.images.all(),
        "files": promotion.files.all(),
    })


@login_required
def image_delete(request, pk):
    image = get_object_or_404(PromotionImage, pk=pk)
    promotion_id = image.promotion.id

    image.image.delete(save=False)  # ลบไฟล์จริง
    image.delete()                  # ลบ record

    messages.success(request, "ลบรูปเรียบร้อยแล้ว")
    return redirect("promotion:edit", promotion_id)


@login_required
def file_delete(request, pk):
    file = get_object_or_404(PromotionFile, pk=pk)
    promotion_id = file.promotion.id

    file.file.delete(save=False)
    file.delete()

    messages.success(request, "ลบไฟล์เรียบร้อยแล้ว")
    return redirect("promotion:edit", promotion_id)
