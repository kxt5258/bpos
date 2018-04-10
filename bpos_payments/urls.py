from bpos_payments import views
from django.contrib.auth.decorators import login_required
from django.conf.urls import url

urlpatterns = [
    url(r'^$', login_required(views.PaymentList.as_view()), name="payment-list"),
    url(r'extraadd/$', login_required(views.create_extra), name="extra-add"),
    url(r'outsadd/$', login_required(views.create_outs), name="outs-add"),
    url(r'add/$', login_required(views.create_payment), name="payment-add"),
    url(r'extra/(?P<pk>[-\w]+)/delete/$$', login_required(views.PayExtraItemDelete.as_view()), name="extra-delete"),
    url(r'outs/(?P<pk>[-\w]+)/delete/$$', login_required(views.PayPaymentOutDelete.as_view()), name="outs-delete"),
    url(r'(?P<pk>[-\w]+)/update/$', login_required(views.update_payment), name="payment-update"),
    url(r'(?P<pk>[-\w]+)/delete/$', login_required(views.PaymentDelete.as_view()), name="payment-update"),
    url(r'(?P<pk>[-\w]+)/$', login_required(views.PaymentDetail.as_view()), name="payment-detail"),
]
