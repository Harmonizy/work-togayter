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