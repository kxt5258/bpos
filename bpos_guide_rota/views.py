from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import GroupGuide
from .forms import GuideRotaForm
from bpos_status_report.models import Client
from bpos_guides.models import Guide
import simplejson


@permission_required('bpos_guide_rota.add_groupguide')
def create_guiderota(request):
    if request.method == 'POST':
        form = GuideRotaForm(request.POST, user=request.user)
        response = {}
        if form.is_valid():
            response["status"] = "OK"
            form.save()
        else:
            response["status"] = "bad"
            response.update(form.errors)

        return HttpResponse(simplejson.dumps(response))
    else:
        form = GuideRotaForm(user=request.user)

    return render(request, 'bpos_guide_rota/guiderota_add.html', {
        'form': form,
    })


@permission_required('bpos_guide_rota.change_groupguide')
def update_guiderota(request, pk):
    if request.method == 'POST':
        guiderota = get_object_or_404(GroupGuide, pk=pk)
        form = GuideRotaForm(request.POST, instance=guiderota, user=request.user)
        response = {}
        if form.is_valid():
            response["status"] = "OK"
            form.save()
        else:
            response["status"] = "bad"
            response.update(form.errors)

        return HttpResponse(simplejson.dumps(response))
    else:
        guiderota = get_object_or_404(GroupGuide, pk=pk)
        form = GuideRotaForm(instance=guiderota, user=request.user)

    return render(request, 'bpos_guide_rota/guiderota_update.html', {
        'form': form,
    })


class GroupGuideList(PermissionRequiredMixin, ListView):
    permission_required = ('bpos_guide_rota.view_groupguide')
    model = GroupGuide
    template_name = "bpos_guide_rota/guiderota_list.html"

    def get_context_data(self, **kwargs):
        context = super(GroupGuideList, self).get_context_data(**kwargs)
        for a in context['object_list']:
            client = Client.objects.get(pk=a.client_id)
            a.start = client.arriving_date
            a.end = client.leaving_date
        return context


class GroupGuideDetail(PermissionRequiredMixin, DetailView):
    permission_required = ('bpos_guide_rota.view_groupguide')
    model = GroupGuide
    template_name = "bpos_guide_rota/guiderota_detail.html"

    def get_context_data(self, **kwargs):
        context = super(GroupGuideDetail, self).get_context_data(**kwargs)
        return context


# Get the trek and other language information of clients
def get_client_information(request):
    response = {}
    if request.GET.get('client_id'):
        client_name = request.GET.get('client_id')
        result = Client.objects.filter(pk=client_name).values("trek", "other_trek", "language", "other_language")

        if result[0]['other_trek']:
            response['trek'] = result[0]['other_trek']
        else:
            response['trek'] = result[0]['trek']

        if result[0]['other_language']:
            response['language'] = result[0]['other_language']
        else:
            response['language'] = result[0]['language']

    return HttpResponse(simplejson.dumps(response))


# Get the filtered list of guides based on the guide filter
def get_filtered_guides(request):
    response = {}
    if request.GET.get('trekking_status'):
        trekking_status = request.GET.get('trekking_status')
        if trekking_status == '0':
            result = Guide.objects.filter().order_by("id")
        else:
            result = Guide.objects.filter(trekking_status=trekking_status).order_by("id")
    else:
        result = Guide.objects.filter().order_by("id")

    for a in result:
        response[a.id] = a.__str__()

    return HttpResponse(simplejson.dumps(response))
