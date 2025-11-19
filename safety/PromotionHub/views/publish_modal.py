from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, render
from PromotionHub.models import Promotion
from django.contrib.auth.models import Group


@login_required
@permission_required("PromotionHub.publish_promotion_hub", raise_exception=True)
def publish_modal(request, pk):
    promotion = get_object_or_404(Promotion, pk=pk)
    groups = Group.objects.all()

    return render(request, "promotion/components/publish_modal.html", {
        "promotion": promotion,
        "groups": groups
    })