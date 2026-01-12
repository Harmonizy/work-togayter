from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib import messages


from .utils import card_data
from ..models import BaseReport
from ..choices import ReportStatusChoices, ReportTypeChoices
from ..rules import q_condition

from common.RTAFAuth.views import SuperAppLoginMixins
from common.RTAFUser.models import Affiliation


@login_required
def view_403(request):
    return render(request, 'Report/safety-reports/403.html')