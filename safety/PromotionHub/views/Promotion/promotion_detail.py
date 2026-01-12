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
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.core.paginator import Paginator

from ...models import Promotion, PromotionView, Quiz, Question, Choice, QuizResult, Document, DocumentFile
from ...forms import PromotionForm, QuizForm, QuestionFormSet, ChoiceFormSet, DocumentForm, DocumentFileForm
from ...choices import PromotionStatusChoices, PromotionPublishChoices, PromotionPriorityChoices, PromotionTypeChoices
from common.RTAFAuth.views import SuperAppLoginMixins
from common.RTAFUser.models import RTAFUser, Affiliation


# @login_required
# def detail(request, pk):
#     promotion = get_object_or_404(Promotion, pk=pk)

#     # ต้องแยกออกเป็นสองตัวแปร ไม่ใช่ตัวเดียว
#     promotion_view, created = PromotionView.objects.get_or_create(
#         user=request.user,
#         promotion=promotion,
#         defaults={'viewed_at': timezone.now()}
#     )

#     view_count = PromotionView.objects.filter(promotion=promotion).count()

#     context = {
#         "promotion": promotion,
#         "promotion_view": promotion_view,  # <- ตอนนี้เป็น instance จริง
#         "view_count": view_count,
#     }
#     return render(request, "PromotionHub/promotion_detail.html", context)


class PromotionDetailView(LoginRequiredMixin, SuperAppLoginMixins, DetailView):
    model = Promotion
    template_name = 'PromotionHub/promotion_detail.html'
    context_object_name = 'promotion'

    def get_object(self, queryset=None):
        obj = Promotion.objects.filter(pk=self.kwargs.get("pk")).first()
        if not obj:
            messages.warning(
                self.request,
                "ประชาสัมพันธ์นี้ถูกลบหรือไม่สามารถเข้าถึงได้"
            )
            raise PermissionDenied
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        promotion = self.object

        promotion_view, created = PromotionView.objects.get_or_create(
            user=self.request.user,
            promotion=promotion,
            defaults={'viewed_at': timezone.now()}
        )

        context['promotion_view'] = promotion_view
        context['view_count'] = PromotionView.objects.filter(
            promotion=promotion
        ).count()

        quiz = promotion.quiz
        if quiz:
            context["quiz"] = quiz
            context["quiz_completed_count"] = quiz.num_completed

            user_done = QuizResult.objects.filter(
                quiz=quiz,
                user=self.request.user
            ).exists()
            context["user_completed_quiz"] = user_done
        else:
            context["quiz"] = None

        return context