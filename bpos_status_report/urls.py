from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from bpos_status_report import views

urlpatterns = [
    url(r'^$', login_required(views.ClientList.as_view()), name="client-list"),
    url(r'udocstatus/$', login_required(views.update_docstatus), name="docstatus"),
    url(r'memberadd/$', login_required(views.create_member), name="member-add"),
    url(r'documentadd/$', login_required(views.create_document), name="document-add"),
    url(r'add/$', login_required(views.create_client), name="client-add"),
    url(r'document/(?P<pk>[-\w]+)/update/$', login_required(views.update_document), name="document-edit"),
    url(r'document/(?P<pk>[-\w]+)/delete/$', login_required(views.DocumentDelete.as_view()), name="document-delete"),
    url(r'member/(?P<pk>[-\w]+)/update/$', login_required(views.update_member), name="member-edit"),
    url(r'member/(?P<pk>[-\w]+)/delete/$', login_required(views.MemberDelete.as_view()), name="member-delete"),
    url(r'(?P<pk>[-\w]+)/update/$', login_required(views.update_client), name="client-update"),
    url(r'(?P<pk>[-\w]+)/delete/$', login_required(views.ClientDelete.as_view()), name="client-delete"),
    url(r'(?P<pk>[-\w]+)/$', login_required(views.ClientDetail.as_view()), name="client-detail"),
]
