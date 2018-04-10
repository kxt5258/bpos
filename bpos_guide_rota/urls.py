from django.conf.urls import url
from bpos_guide_rota import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', login_required(views.GroupGuideList.as_view()), name="guiderota-list"),
    url(r'add/$', login_required(views.create_guiderota), name="guiderota-add"),
    url(r'(?P<pk>[-\w]+)/update/$', login_required(views.update_guiderota), name="guiderota-update"),
    url(r'(?P<pk>[-\w]+)/$', login_required(views.GroupGuideDetail.as_view()), name="guiderota-detail"),
    url(r'^get_client_info', login_required(views.get_client_information), name="guiderota_get_client_information"),
    url(r'^get_filtered_guides', login_required(views.get_filtered_guides), name="guiderota_get_filtered_guides")
]
