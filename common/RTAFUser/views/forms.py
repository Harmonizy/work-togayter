from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from ..forms import RTAFUserForm
from ..models.choices import DataStatus

class RTAFUserCreateView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            'user_form':RTAFUserForm(instance = request.user),            
        }
        return render(request, 'RTAFUser/user_create.html', context)
    
    def post(self, request):
        user_form = RTAFUserForm(request.POST, instance=request.user)
        
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.data_status = DataStatus.SELF
            user.login_limited = -1
            user.save()
        
            context = {
                'user': user,                
            }
            return render(request, 'RTAFUser/user_create_success.html', context)
        return render(request, 'RTAFUser/user_create.html', {'user_form': user_form})