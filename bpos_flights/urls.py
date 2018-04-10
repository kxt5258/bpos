from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from bpos_flights import views

urlpatterns = [
    url(r'^$', login_required(views.FlightList.as_view()), name="flight-list"),
    url(r'plist/(?P<pk>[-\w]+)/$', login_required(views.PassengerList.as_view()), name="passenger-list"),
    url(r'passenger/add/$', login_required(views.create_flight), name="flight-add"),
    url(r'add/$', login_required(views.create_flightgroup), name="passenger-add"),
    url(r'passenger/(?P<pk>[-\w]+)/update/$', login_required(views.update_flight), name="passenger-update"),
    url(r'passenger/(?P<pk>[-\w]+)/delete/$', login_required(views.FlightDelete.as_view()), name="passenger-delete"),
    url(r'(?P<pk>[-\w]+)/update/$', login_required(views.update_flightgroup), name="flight-update"),
    url(r'(?P<pk>[-\w]+)/$', login_required(views.FlightDetail.as_view()), name="flight-detail"),
    url(r'get_passenger_info', login_required(views.get_passenger_info)),
    url(r'get_filtered_passengers', login_required(views.get_filtered_passengers)),
    url(r'get_filtered_clients', login_required(views.get_filtered_clients))
]
