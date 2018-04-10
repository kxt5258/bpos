from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
import simplejson

from django.views.generic.list import ListView
from .models import Enquiry
from .forms import EnquiryForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

from bpos_status_report.models import Client
from bpos_agents.models import Agent
from django.utils import timezone


@permission_required('bpos_enquiries.add_enquiry')
def create_enquiry(request):
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        response = {}
        if form.is_valid():
            response["status"] = "OK"
            form.save()
        else:
            response["status"] = "bad"
        return HttpResponse(simplejson.dumps(response))
    else:
        form = EnquiryForm()

    return render(request, 'bpos_enquiries/enquiry_add.html', {
        'form': form,
    })


@permission_required('bpos_enquiries.change_enquiry')
def update_enquiry(request, pk):
    if request.method == 'POST':
        enquiry = get_object_or_404(Enquiry, pk=pk)
        form = EnquiryForm(request.POST, instance=enquiry)
        response = {}
        if form.is_valid():
            response["status"] = "OK"
            f = form.save()
            if form.cleaned_data['status'] == "confirmed":
                en_list = enquiry.clients.all()
                if not en_list:
                    client_data = {
                        # make sure pk of BP is 1
                        'agent': get_object_or_404(Agent, pk=1),
                        'type': 'fit',
                        'group_name': enquiry.full_name,
                        'arriving_date': timezone.now(),
                        'leaving_date': timezone.now(),
                        'language_guide_needed': 0,
                        'enquiry': enquiry
                    }
                    client = Client(**client_data)
                    client.save()
                    f.client_id = client.pk
                    f.save()
        else:
            response["status"] = "bad"
            response.update(form.errors)

        return HttpResponse(simplejson.dumps(response))
    else:
        enquiry = get_object_or_404(Enquiry, pk=pk)
        form = EnquiryForm(instance=enquiry)

    return render(request, 'bpos_enquiries/enquiry_update.html', {
        'form': form,
    })


class EnquiryList(PermissionRequiredMixin, ListView):
    permission_required = ('bpos_enquiries.view_enquiry')
    model = Enquiry
    template_name = "bpos_enquiries/enquiry_list.html"

    def get_context_data(self, **kwargs):
        context = super(EnquiryList, self).get_context_data(**kwargs)
        return context
