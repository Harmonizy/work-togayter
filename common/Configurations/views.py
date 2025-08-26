from django.shortcuts import render

from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy


from .models import Config


class ConfigListView(ListView):
    model = Config
    template_name = 'Configurations/config_list.html'
    context_object_name = 'configs'


class ConfigCreateView(CreateView):
    model = Config
    fields = ['key', 'value', 'description']
    template_name = 'Configurations/config_form.html'
    success_url = reverse_lazy('Configurations:list')


class ConfigUpdateView(UpdateView):
    model = Config
    fields = ['value', 'description']
    template_name = 'Configurations/config_form.html'
    success_url = reverse_lazy('Configurations:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = self.object.key
        return context