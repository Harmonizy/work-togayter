from urllib.parse import urlencode

from django.views import View
from django.shortcuts import render, redirect, reverse

from .models import QRImageData, QRScan
from common.RTAFAuth.views import SuperAppLoginMixins

class HubSuperAppView(SuperAppLoginMixins, View):
    def redirect_success_url(self, request):
        payload = request.session.get("payload", {})
        qr_image_data = QRImageData.objects.get(token=payload.get("qr_data", ""))
        url = reverse(qr_image_data.type.url_redirect, kwargs={qr_image_data.type.object_id_name: qr_image_data.object_id})
        
        params = dict(zip(qr_image_data.type.keys, qr_image_data.args)) if qr_image_data.args else {}
        if params:
            url = f"{url}?{urlencode(params)}"
            
        QRScan.objects.create(qr_image_data=qr_image_data, scanner=request.user)
        
        return redirect(url)
