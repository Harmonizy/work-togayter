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
    
    paginator = Paginator(promotions, 10)  # 10 รายการต่อหน้า
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "promotions": page_obj,
        "page_obj": page_obj, 
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

    paginator = Paginator(promotions, 10)  # 10 รายการต่อหน้า
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "promotions": page_obj,
        "page_obj": page_obj, 
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

    paginator = Paginator(promotions, 10)  # 10 รายการต่อหน้า
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "promotions": page_obj,
        "page_obj": page_obj, 
        "type": "การแจ้งเตือน"
    }
    return render(request, "PromotionHub/promotion_list.html", context)