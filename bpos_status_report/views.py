
# Create your views here.
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
import simplejson

from .models import Client, Member, Document
from .forms import ClientForm, ClientEditForm, MemberForm, DocumentForm


@permission_required('bpos_status_report.add_client')
def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        response = {}
        if form.is_valid():
            response["status"] = "OK"
            form.save()
        else:
            response["status"] = "bad"
            response.update(form.errors)
        return HttpResponse(simplejson.dumps(response))
    else:
        form = ClientForm()

    return render(request, 'bpos_status_report/status_add.html', {
        'form': form,
    })


@permission_required('bpos_status_report.change_client')
def update_client(request, pk):
    if request.method == 'POST':
        enquiry = get_object_or_404(Client, pk=pk)
        form = ClientEditForm(request.POST, instance=enquiry)
        response = {}
        if form.is_valid():
            response["status"] = "OK"
            form.save()
        else:
            response["status"] = "bad"
            response.update(form.errors)

        return HttpResponse(simplejson.dumps(response))
    else:
        enquiry = get_object_or_404(Client, pk=pk)
        form = ClientEditForm(instance=enquiry)

    return render(request, 'bpos_status_report/status_update.html', {
        'form': form,
    })


class ClientDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('bpos_status_report.delete_client')
    model = Client
    success_url = reverse_lazy("client-list")
    template_name = "common/delete_form.html"


class ClientList(PermissionRequiredMixin, ListView):
    permission_required = ('bpos_status_report.view_client')
    model = Client
    template_name = "bpos_status_report/status_list.html"

    def get_context_data(self, **kwargs):
        context = super(ClientList, self).get_context_data(**kwargs)
        return context


class ClientDetail(PermissionRequiredMixin, DetailView):
    permission_required = ('bpos_status_report.view_client')
    model = Client
    template_name = "bpos_status_report/status_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ClientDetail, self).get_context_data(**kwargs)
        context['member_list'] = Member.objects.filter(client=context['object'].id).order_by("id")
        context['document_list'] = Document.objects.filter(client=context['object'].id).order_by("id")
        return context


@permission_required('bpos_status_report.add_member')
def create_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        response = {}
        if form.is_valid():
            form.save()
            response["status"] = "OK"
        else:
            response["status"] = "bad"
            response.update(form.errors)
        return HttpResponse(simplejson.dumps(response))
    else:
        '''Initialize the client value and disable others in view'''
        if request.GET['client']:
            form = MemberForm(initial={"client": request.GET['client']})
        else:
            form = MemberForm()

    return render(request, 'bpos_status_report/member/member_add.html', {
        'form': form,
    })


@permission_required('bpos_status_report.change_member')
def update_member(request, pk):
    if request.method == 'POST':
        member = get_object_or_404(Member, pk=pk)
        form = MemberForm(request.POST, instance=member)
        response = {}
        if form.is_valid():
            form.save()
            response["status"] = "OK"
        else:
            response["status"] = "bad"
            response.update(form.errors)
        return HttpResponse(simplejson.dumps(response))
    else:
        '''Initialize the client value and disable others in view'''
        member = get_object_or_404(Member, pk=pk)
        form = MemberForm(instance=member)

    return render(request, 'bpos_status_report/member/member_add.html', {
        'form': form,
    })


class MemberDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('bpos_status_report.delete_member')
    model = Member
    template_name = "common/delete_form.html"

    def post(self, request, *args, **kwargs):
        self.success_url = request.POST['parent_url']
        return self.delete(request, *args, **kwargs)


@permission_required('bpos_status_report.add_document')
def create_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, label="Create Document")
        print(request.FILES)
        response = {}
        if form.is_valid():
            doc = form.save()
            return redirect(doc.client)

        else:
            response["status"] = "bad"
            response.update(form.errors)
        return HttpResponse(simplejson.dumps(response))
    else:
        '''Initialize the client value and disable others in view'''
        if request.GET['client']:
            form = DocumentForm(initial={"client": request.GET['client']}, label="Create Document")
        else:
            form = DocumentForm(label="Create Document")

    return render(request, 'bpos_status_report/document/document_add.html', {
        'form': form,
    })


@permission_required('bpos_status_report.change_document')
def update_document(request, pk):
    if request.method == 'POST':
        document = get_object_or_404(Document, pk=pk)
        form = DocumentForm(request.POST, request.FILES, instance=document, label="Update Document")
        response = {}
        if form.is_valid():
            doc = form.save()
            return redirect(doc.client)
        else:
            response["status"] = "bad"
            response.update(form.errors)
        return HttpResponse(simplejson.dumps(response))
    else:
        '''Initialize the client value and disable others in view'''
        document = get_object_or_404(Document, pk=pk)
        form = DocumentForm(instance=document, label="Update Document")

    return render(request, 'bpos_status_report/document/document_add.html', {
        'form': form,
    })


class DocumentDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('bpos_status_report.delete_document')
    model = Document
    template_name = "common/delete_form.html"

    def post(self, request, *args, **kwargs):
        self.success_url = request.POST['parent_url'] + "#visa_document"
        return self.delete(request, *args, **kwargs)


def update_docstatus(request):
    if request.method == 'POST':
        id = request.POST.get('client')
        status = request.POST.get('status')
        client = Client.objects.get(pk=id)
        if not status:
            status = 0
        client.status = status
        client.save()
        response = {"status": "done"}
    return HttpResponse(simplejson.dumps(response))
