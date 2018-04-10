from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from bpos_enquiries import views

urlpatterns = [
    url(r'^$', login_required(views.EnquiryList.as_view()), name="enquiry-list"),
    url(r'add/$', login_required(views.create_enquiry), name="enquiry-add"),
    url(r'(?P<pk>[-\w]+)/update/$', login_required(views.update_enquiry), name="enquiry-update"),
]
