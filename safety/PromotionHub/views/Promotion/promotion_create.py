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
def create_ground(request):
    if request.method == "POST":
        form = PromotionForm(request.POST, request.FILES)
        if form.is_valid():
            promotion = form.save(commit=False)
            promotion.user = request.user
            promotion.priority = PromotionPriorityChoices.NONE
            promotion.type = PromotionTypeChoices.GROUND
            promotion.save()

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

            messages.success(request, "สร้างบทความใหม่เรียบร้อยแล้ว!")
            return redirect("promotion:list_ground")
        else:
            messages.error(request, "ไม่สามารถบันทึกได้ กรุณาตรวจสอบข้อมูลอีกครั้ง")
    else:
        form = PromotionForm()

    return render(request, "PromotionHub/promotion_create.html", {
        "form": form,
        "type": "ภาคพื้น"
    })


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

            messages.success(request, "สร้างบทความใหม่เรียบร้อยแล้ว!")
            return redirect("promotion:list_air")
        else:
            messages.error(request, "ไม่สามารถบันทึกได้ กรุณาตรวจสอบข้อมูลอีกครั้ง")
    else:
        form = PromotionForm()

    return render(request, "PromotionHub/promotion_create.html", {
        "form": form,
        "type": "การบิน"
    })


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


            messages.success(request, "สร้างบทความใหม่เรียบร้อยแล้ว!")
            return redirect("promotion:announcement_list")
        else:
            messages.error(request, "ไม่สามารถบันทึกได้ กรุณาตรวจสอบข้อมูลอีกครั้ง")
    else:
        form = PromotionForm()

    return render(request, "PromotionHub/promotion_create.html", {
        "form": form,
        "type": "การแจ้งเตือน"
    })

