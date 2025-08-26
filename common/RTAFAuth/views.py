from datetime import datetime

from django.contrib.auth import authenticate , login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, HttpResponse
from django.http import HttpResponseRedirect

# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token



# from common.RTAFUser.serializers import ShortRTAFUserSerializer as UserSerializer


from .forms import MyAuthForm
from .backends import SuperAppBackend as Backend


class SuperAppLoginMixins:
    def redirect_success_url(self, request):
        return redirect(self.get_success_url())
    
    def get(self, request, *args, **kwargs):
        salt = request.GET.get('ref_token')
        print("SuperAppLoginMixins get called")
        if salt:
            print("Salt token:", salt)
            user = Backend().authenticate(request, username="super-app-salt-auth", password=salt)
            print("User authenticated:", user)
            if user:
                login(request, user, backend='common.RTAFAuth.backends.SuperAppBackend')
                # setup_user(request, user)
                return self.redirect_success_url(request)
            
            print("Authentication failed")
            return HttpResponse("การยืนยันผ่าน Super App fail", status=401)

        return super().get(request, *args, **kwargs)


class AFLoginView(SuperAppLoginMixins, LoginView):
    template_name = 'account/login.html'
    form_class = MyAuthForm

    def get(self, request, *args, **kwargs):        
        
        if request.GET.get("ref"):
            print("ref = ", request.GET.get("ref"))
            user = authenticate(request, username=request.GET.get("ref"), password="-")
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(self.get_success_url())        

        return super().get(request, *args, **kwargs)


class SuperAppLoginView(SuperAppLoginMixins, LoginView):
    pass


# class AuthTokenWithRTAFUser(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         user.last_login = datetime.now()
#         user.save()
#         token, _ = Token.objects.get_or_create(user=user)
#         user_data = UserSerializer(user).data
#         user_data['token'] = token.key

#         return Response(user_data)