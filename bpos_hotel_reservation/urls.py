from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from bpos_hotel_reservation import views

urlpatterns = [
    url(r'^$', login_required(views.HotelList.as_view()), name="hotel-list"),
    url(r'roomadd/$', login_required(views.create_room), name="room-add"),
    url(r'add/$', login_required(views.create_hotel), name="hotel-add"),
    url(r'roomupdate/(?P<pk>[-\w]+)/update/$', login_required(views.update_room), name="room-update"),
    url(r'roomupdate/(?P<pk>[-\w]+)/delete/$', login_required(views.RoomDelete.as_view()), name="room-delete"),
    url(r'(?P<pk>[-\w]+)/update/$', login_required(views.update_hotel), name="hotel-update"),
    url(r'(?P<pk>[-\w]+)/delete/$', login_required(views.delete_hotel), name="hotel-delete"),
    url(r'(?P<pk>[-\w]+)/$', login_required(views.HotelDetail.as_view()), name="hotel-detail"),
    url(r'^get_filtered_hotels', login_required(views.get_filtered_hotels), name="hotel-get_filtered_hotels")
]
