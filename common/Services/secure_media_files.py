import mimetypes
import os

from django.http import HttpResponse, Http404
from django.conf import settings
from django.contrib.auth.decorators import login_required


def check_user_access(user, path):
    conditions = [        
        lambda: user.is_superuser,
        # lambda: user.profile.is_approved if hasattr(user, 'profile') else False,
        
        # lambda: user.subscription_level == 'premium',
        
        # You can add more dynamic conditions here
        # Example: lambda: user.groups.filter(name='VIP').exists(),
    ]
    
    return all(condition() for condition in conditions)


@login_required
def serve_secure_media(request, path):

    if not check_user_access(request.user, path):
        raise Http404
        
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    if not os.path.exists(file_path):
        raise Http404

    mime_type, _ = mimetypes.guess_type(file_path)

    if mime_type is None:
        mime_type = "application/octet-stream"

    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type=mime_type)
        response['Content-Disposition'] = f'inline; filename={os.path.basename(file_path)}'
        return response
