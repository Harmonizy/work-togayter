from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.urls import reverse_lazy

from ..models import Affiliation, Rank
from ..forms import AffiliationForm

class AffiliationListView(ListView):
    model = Affiliation
    template_name = 'RTAFUser/affiliation_list.html'
    context_object_name = 'affiliations'
    # paginate_by = 20


class AffiliationDetailView(DetailView):
    model = Affiliation
    template_name = 'RTAFUser/affiliation_detail.html' 
    context_object_name = 'affiliation'


class AffliationUpdateView(UpdateView):
    model = Affiliation
    template_name = 'RTAFUser/affiliation_update.html'
    context_object_name = 'affiliation'
    form_class = AffiliationForm
    success_url = reverse_lazy('RTAFUser:affiliation_list')


class AffiliationCreateView(CreateView):
    model = Affiliation
    template_name = 'RTAFUser/affiliation_create.html'
    context_object_name = 'affiliation'
    form_class = AffiliationForm
    success_url = reverse_lazy('RTAFUser:affiliation_list')