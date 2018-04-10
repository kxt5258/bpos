
# Create your views here.
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import DeleteView
import simplejson

from .models import HotelReservation, Room
from .forms import RoomForm, HotelForm
from bpos_hotels.models import Hotel


@permission_required('bpos_hotel_reservation.add_hotelreservation')
def create_hotel(request):
    if request.method == 'POST':
        form = HotelForm(request.POST)
        response = {}
        if form.is_valid():
            response["status"] = "OK"
            form.save()
        else:
            response["status"] = "bad"
            response.update(form.errors)
        return HttpResponse(simplejson.dumps(response))
    else:
        form = HotelForm()

    return render(request, 'bpos_hotel_reservation/hotels_add.html', {
        'form': form,
    })


@permission_required('bpos_hotel_reservation.change_hotelreservation')
def update_hotel(request, pk):
    if request.method == 'POST':
        enquiry = get_object_or_404(HotelReservation, pk=pk)
        form = HotelForm(request.POST, instance=enquiry)
        response = {}
        if form.is_valid():
            response["status"] = "OK"
            form.save()
        else:
            response["status"] = "bad"
            response.update(form.errors)

        return HttpResponse(simplejson.dumps(response))
    else:
        enquiry = get_object_or_404(HotelReservation, pk=pk)
        form = HotelForm(instance=enquiry)

    return render(request, 'bpos_hotel_reservation/hotels_update.html', {
        'form': form,
    })


@permission_required('bpos_hotel_reservation.delete_hotelreservation')
def delete_hotel(request, pk):
    # Delete logic
    response = {"status": "OK"}
    return HttpResponse(simplejson.dumps(response))


class HotelList(ListView):
    model = HotelReservation
    template_name = "bpos_hotel_reservation/hotels_list.html"

    def get_context_data(self, **kwargs):
        context = super(HotelList, self).get_context_data(**kwargs)
        return context


class HotelDetail(DetailView):
    model = HotelReservation
    template_name = "bpos_hotel_reservation/hotels_detail.html"

    def get_context_data(self, **kwargs):
        context = super(HotelDetail, self).get_context_data(**kwargs)
        context['room_list'] = Room.objects.filter(hotel=context['object'].id).order_by("id")
        return context


@permission_required('bpos_hotel_reservation.add_room')
def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
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
        if request.GET['hotel']:
            form = RoomForm(initial={"hotel": request.GET['hotel']})
        else:
            form = RoomForm()

    return render(request, 'bpos_hotel_reservation/room_add.html', {
        'form': form,
    })


@permission_required('bpos_hotel_reservation.change_room')
def update_room(request, pk):
    if request.method == 'POST':
        enquiry = get_object_or_404(Room, pk=pk)
        form = RoomForm(request.POST, instance=enquiry)
        response = {}
        if form.is_valid():
            response["status"] = "OK"
            form.save()
        else:
            response["status"] = "bad"
            response.update(form.errors)

        return HttpResponse(simplejson.dumps(response))
    else:
        enquiry = get_object_or_404(Room, pk=pk)
        form = RoomForm(instance=enquiry)

    return render(request, 'bpos_hotel_reservation/room_add.html', {
        'form': form,
    })


class RoomDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('bpos_hotel_reservation.delete_room')
    model = Room
    template_name = "common/delete_form.html"

    def post(self, request, *args, **kwargs):
        self.success_url = request.POST['parent_url']
        return self.delete(request, *args, **kwargs)


# Get the filtered list of guides based on the guide filter
def get_filtered_hotels(request):
    response = {}
    hotel_type = request.GET.get('hotel_type')
    town = request.GET.get('town')
    if hotel_type and town:
            result = Hotel.objects.filter(type=hotel_type, town=town).order_by("id")
    elif town:
            result = Hotel.objects.filter(town=town).order_by("id")
    elif hotel_type:
            result = Hotel.objects.filter(type=hotel_type).order_by("id")
    else:
        result = Hotel.objects.filter().order_by("id")

    for a in result:
        response[a.id] = a.__str__()

    return HttpResponse(simplejson.dumps(response))
