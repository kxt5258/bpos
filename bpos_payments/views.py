from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from .models import Payment, PayExtraItem, PayPaymentOut
from .forms import PaymentForm, ExtraItemForm, PaymentOutsForm
import simplejson


@permission_required('bpos_payments.add_payment')
def create_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES, label="Create Payment")
        response = {}
        if form.is_valid():
            response["status"] = "OK"
            object = form.save()
            return redirect(object)

        else:
            response["status"] = "bad"
            response.update(form.errors)

        return HttpResponse(simplejson.dumps(response))
    else:
            form = PaymentForm(label="Create Payment")
    return render(request, 'bpos_payments/payments_add.html', {
        'form': form,
    })


@permission_required('bpos_payments.change_payment')
def update_payment(request, pk):
    if request.method == 'POST':
        payment = get_object_or_404(Payment, pk=pk)
        form = PaymentForm(request.POST, request.FILES, instance=payment, label="Update Payment")
        response = {}
        if form.is_valid():
            response["status"] = "OK"
            form.save()
            return redirect(payment)
        else:
            response["status"] = "bad"
            response.update(form.errors)

        return HttpResponse(simplejson.dumps(response))
    else:
        flights = get_object_or_404(Payment, pk=pk)
        form = PaymentForm(instance=flights, label="Update Payment")

    return render(request, 'bpos_payments/payments_add.html', {
        'form': form,
    })


class PaymentDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('bpos_payments.delete_payment')
    model = Payment
    success_url = reverse_lazy("payment-list")
    template_name = "common/delete_form.html"


@permission_required('bpos_payments.add_payextraitem')
def create_extra(request):
    if request.method == 'POST':
        form = ExtraItemForm(request.POST)
        response = {}
        if form.is_valid():
            response["status"] = "OK"
            form.save()

        else:
            response["status"] = "bad"
            response.update(form.errors)

        return HttpResponse(simplejson.dumps(response))
    else:
        if request.GET['client']:
            form = ExtraItemForm(initial={"client": request.GET['client']})
        else:
            form = ExtraItemForm()
    return render(request, 'bpos_payments/items_add.html', {
        'form': form,
    })


class PayExtraItemDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('bpos_payments.delete_payextraitem')
    model = PayExtraItem
    template_name = "common/delete_form.html"

    def post(self, request, *args, **kwargs):
        self.success_url = request.POST['parent_url']
        return self.delete(request, *args, **kwargs)


class PayPaymentOutDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('bpos_payments.delete_paypaymentout')
    model = PayPaymentOut
    template_name = "common/delete_form.html"

    def post(self, request, *args, **kwargs):
        self.success_url = request.POST['parent_url']
        return self.delete(request, *args, **kwargs)


@permission_required('bpos_payments.add_paypaymentout')
def create_outs(request):
    if request.method == 'POST':
        form = PaymentOutsForm(request.POST)
        response = {}
        if form.is_valid():
            response["status"] = "OK"
            form.save()

        else:
            response["status"] = "bad"
            response.update(form.errors)

        return HttpResponse(simplejson.dumps(response))
    else:
        if request.GET['client']:
            form = PaymentOutsForm(initial={"client": request.GET['client']})
        else:
            form = PaymentOutsForm()
    return render(request, 'bpos_payments/items_add.html', {
        'form': form,
    })


class PaymentList(PermissionRequiredMixin, ListView):
    permission_required = ('bpos_payments.view_payment')
    model = Payment
    template_name = "bpos_payments/payments_list.html"

    def get_Scontext_data(self, **kwargs):
        context = super(PaymentList, self).get_context_data(**kwargs)
        for a in context['object_list']:
            payment_status = ''
            if a.payment:
                payment_status = "Payment - " + str(a.get_payment_display)
            if a.balance:
                payment_status = "Balance - " + str(a.get_balance_display)
            if a.deposit:
                payment_status = "Deposit - " + str(a.get_deposit_display)
            a.payment_status = payment_status
        return context


class PaymentDetail(PermissionRequiredMixin, DetailView):
    permission_required = ('bpos_payments.view_payment')
    model = Payment
    template_name = "bpos_payments/payments_detail.html"

    def get_context_data(self, **kwargs):
        context = super(PaymentDetail, self).get_context_data(**kwargs)
        context['extra_list'] = PayExtraItem.objects.filter(client=context['object'].client_id)
        context['outs_list'] = PayPaymentOut.objects.filter(client=context['object'].client_id)
        return context
