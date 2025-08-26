from django import template
from django.shortcuts import get_object_or_404

from common.SuperAppQR.models import QRType, QRImageData

register = template.Library()

@register.inclusion_tag('SuperAppQR/qr-image.html')
def show_qr_image(qr_id):
    qr_image = QRImageData.objects.get(id = qr_id)
    return {'qr_image': qr_image}


@register.inclusion_tag('SuperAppQR/qr-image.html')
def generate_qr_by_object_id(qr_size, type_text, object_id, *args):
    qr_type = get_object_or_404(QRType, name=type_text)    
    qr_image, created = QRImageData.objects.get_or_create(
        type=qr_type,
        object_id=object_id,
        defaults={
            "args": args,
        }
    )
    return {'qr_size': qr_size, 'code': qr_image.qr_text()}
