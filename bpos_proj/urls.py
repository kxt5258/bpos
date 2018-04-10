"""bpos_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from bpos_proj import views
from bpos_proj.forms import LoginForm
from django.contrib.auth import views as auth_view
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^$', views.home, name='home-page'),
    url(r'^api/enquiry_data/$', views.get_enquiry_data, name='enquiry-page'),
    url(r'^login/$', auth_view.login, {'template_name': 'registration/login.html', 'authentication_form': LoginForm}, name="login"),
    url(r'^logout/$', auth_view.LogoutView.as_view(next_page=reverse_lazy('login')), name="logout"),
    url(r'^admin/', admin.site.urls),
    url(r'^client-autocomplete/', login_required(views.ClientAutocomplete.as_view()), name="client-autocomplete"),
    url(r'^mgmtdata/', views.mgmtdata, name='mgmtdata'),
    url(r'^enquiries/', include('bpos_enquiries.urls')),
    url(r'^status/', include('bpos_status_report.urls')),
    url(r'^guiderota/', include('bpos_guide_rota.urls')),
    url(r'^flights/', include('bpos_flights.urls')),
    url(r'^payments/', include('bpos_payments.urls')),
    url(r'^hotels/', include('bpos_hotel_reservation.urls'))
]
