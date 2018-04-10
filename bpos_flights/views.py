from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import DeleteView

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Flight, FlightGroup
from .forms import FlightForm, FlightGroupForm
from bpos_status_report.models import Member, Client

from dateutil.relativedelta import relativedelta
import simplejson


@permission_required('bpos_flights.add_flight')
def create_flight(request):
    if request.method == 'POST':
        form = FlightForm(request.POST)
        response = {}
        if form.is_valid():
            response["status"] = "OK"
            form.save()

        else:
            response["status"] = "bad"
            response.update(form.errors)

        return HttpResponse(simplejson.dumps(response))
    else:
        # Initialize the client value and disable others in view
        if request.GET['client']:
            form = FlightForm(initial={"client": request.GET['client']})
        else:
            form = FlightForm()
    return render(request, 'bpos_flights/passenger/passenger_add.html', {
        'form': form,
    })


@permission_required('bpos_flights.change_flight')
def update_flight(request, pk):
    if request.method == 'POST':
        flights = get_object_or_404(Flight, pk=pk)
        form = FlightForm(request.POST, instance=flights)
        response = {}
        if form.is_valid():
            response["status"] = "OK"
            form.save()
        else:
            response["status"] = "bad"
            response.update(form.errors)

        return HttpResponse(simplejson.dumps(response))
    else:
        flights = get_object_or_404(Flight, pk=pk)
        form = FlightForm(instance=flights)

    return render(request, 'bpos_flights/passenger/passenger_update.html', {
        'form': form,
    })


class FlightDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('bpos_flights.delete_flight')
    model = Flight
    template_name = "common/delete_form.html"

    def post(self, request, *args, **kwargs):
        self.success_url = request.POST['parent_url']
        return self.delete(request, *args, **kwargs)


class FlightList(ListView):
    model = FlightGroup
    template_name = "bpos_flights/flights_list.html"

    def get_context_data(self, **kwargs):
        context = super(FlightList, self).get_context_data(**kwargs)
        for a in context['object_list']:
            fl = Flight.objects.filter(client=a.client).values("ttl").order_by("-ttl")[:1]
            if fl:
                a.ttl = fl[0]['ttl']
        return context


class PassengerList(ListView):
    model = Flight
    template_name = "bpos_flights/passenger/passenger_list.html"

    def get_context_data(self, **kwargs):
        context = super(PassengerList, self).get_context_data(**kwargs)
        pk_id = self.kwargs.get('pk', None)
        if pk_id:
            context['client'] = FlightGroup.objects.get(pk=pk_id)
            context['object_list'] = context['object_list'].filter(client=context['client'].client)
            for a in context['object_list']:
                if(relativedelta(a.date, a.dob).years < 12):
                    a.is_child = 1
                else:
                    a.is_child = 0
        else:
            context['client'] = None
            context['object_list'] = None

        return context


class FlightDetail(DetailView):
    model = Flight
    template_name = "bpos_flights/flights_detail.html"

    def get_context_data(self, **kwargs):
        context = super(FlightDetail, self).get_context_data(**kwargs)
        return context


@permission_required('bpos_flights.add_flightgroup')
def create_flightgroup(request):
    if request.method == 'POST':
        form = FlightGroupForm(request.POST)
        response = {}
        if form.is_valid():
            response["status"] = "OK"
            form.save()
        else:
            response["status"] = "bad"
            response.update(form.errors)

        return HttpResponse(simplejson.dumps(response))
    else:
        form = FlightGroupForm()

    return render(request, 'bpos_flights/flights_add.html', {
        'form': form,
    })


@permission_required('bpos_flights.change_flightgroup')
def update_flightgroup(request, pk):
    if request.method == 'POST':
        flights = get_object_or_404(FlightGroup, pk=pk)
        form = FlightGroupForm(request.POST, instance=flights)
        response = {}
        if form.is_valid():
            response["status"] = "OK"
            form.save()
        else:
            response["status"] = "bad"
            response.update(form.errors)

        return HttpResponse(simplejson.dumps(response))
    else:
        flights = get_object_or_404(FlightGroup, pk=pk)
        form = FlightGroupForm(instance=flights)

    return render(request, 'bpos_flights/flights_update.html', {
        'form': form,
    })


# Get the filtered list of clients for on the client filter
def get_filtered_clients(request):
    response = {}
    if request.GET.get('trekking_status'):
        client_obj = request.GET.get('trekking_status')
        if client_obj == '0':
            result = Client.objects.filter().order_by("id")
        else:
            result = Client.objects.filter(trekking_status=client_obj).order_by("id")
    else:
        result = Client.objects.filter().order_by("id")

    for a in result:
        response[a.id] = a.__str__()

    return HttpResponse(simplejson.dumps(response))


# Get the filtered list of passengers based on the client filter
def get_filtered_passengers(request):
    response = {}
    if request.GET.get('client_filter'):
        client_obj = request.GET.get('client_filter')
        if client_obj == '0':
            result = Member.objects.filter().order_by("id")
        else:
            result = Member.objects.filter(client=client_obj).order_by("id")
    else:
        result = Member.objects.filter().order_by("id")

    for a in result:
        response[a.id] = a.__str__()

    return HttpResponse(simplejson.dumps(response))


# Get the Passenger Info
def get_passenger_info(request):
    response = {}
    if request.GET.get('pass_id'):
        client_name = request.GET.get('pass_id')
        result = Member.objects.filter(pk=client_name).values("title", "full_name")
        response['title'] = result[0]['title']
        response['full_name'] = result[0]['full_name']

    return HttpResponse(simplejson.dumps(response))
