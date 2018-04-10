from django.shortcuts import render
from dal import autocomplete
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from bpos_enquiries.models import Enquiry
from bpos_status_report.models import Client
from bpos_agents.models import Agent


@login_required(login_url='/login/')
def home(request):
    context = {"title": "BPOS"}
    return render(request, "common/home.html", context)


@login_required(login_url='/login/')
def mgmtdata(request):
    client_list = Client.objects.filter(is_archive=1).order_by("arriving_date")
    context = {"title": "Management Data", "client_list": client_list}
    return render(request, "common/mgmtdata.html", context)


def get_enquiry_data(request, *args, **kwargs):
    en_label = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    en_total = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    en_confirmed = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    client_label = ["Agent Group", "Agent FIT", "BP Group/FIT"]
    client_data = [0, 0, 0]
    by_agent_label = ["Agent", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Total"]
    by_agent_data = {}

    year = request.GET.get('year')

    if year == '0000':
        en_data = Enquiry.objects.raw("select id, created_on, count(*) as num, strftime('%m', created_on) as \
                                       month from bpos_enquiries_enquiry group by month;")
    else:
        en_data = Enquiry.objects.raw("select id, created_on, count(*) as num, strftime('%m', created_on) as \
                                       month from bpos_enquiries_enquiry where created_on between \'" + str(year) + "-01-01\' \
                                       and \'" + str(year) + "-12-31\' group by month;")

    calculate_per_month(en_data, en_total)

    if year == '0000':
        con_data = Enquiry.objects.raw("select id, created_on, count(*) as num, strftime('%m', created_on) as month\
                                       from bpos_enquiries_enquiry where confirmed_on is not null group by month;")
    else:
        con_data = Enquiry.objects.raw("select id, created_on, count(*) as num, strftime('%m', created_on) as \
                                       month from bpos_enquiries_enquiry where created_on between \'" + str(year) + "-01-01\' \
                                       and \'" + str(year) + "-12-31\' and confirmed_on is not null group by month;")

    calculate_per_month(con_data, en_confirmed)

    if year == '0000':
        clients = Client.objects.raw("select id, arriving_date, sum(pax) as num, strftime('%m', arriving_date) as month,\
                                     agent, type from bpos_status_report_client group by month, agent, type;")
    else:
        clients = Client.objects.raw("select id, arriving_date, sum(pax) as num, strftime('%m', arriving_date) as month,\
                                      agent_id, type from bpos_status_report_client where arriving_date between \'" + str(year) + "-01-01\' \
                                      and \'" + str(year) + "-12-31\' group by agent_id, type;")

    calculate_client_total(clients, client_data)

    if year == '0000':
        by_agent = Client.objects.raw("select id, arriving_date, sum(pax) as num, strftime('%m', arriving_date) as month,\
                                     agent from bpos_status_report_client group by month, agent;")
    else:
        by_agent = Client.objects.raw("select a.id, sum(a.pax) as num, strftime('%m', a.arriving_date) as month,\
                                      b.name as agent_name, a.agent_id as agent_id from bpos_status_report_client a join bpos_agents_agent b on a.agent_id = b.id where a.arriving_date between \'" + str(year) + "-01-01\' \
                                      and \'" + str(year) + "-12-31\' group by agent_id, month;")

    segragate_by_client(by_agent, by_agent_data)

    # Include agents even without any clients
    all_agents = Agent.objects.all()
    all_agent_data = by_agent_data.copy()

    agent_total_per_month = ["Total", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Total them up
    for a in all_agent_data:
        for x in range(1, 14):
            agent_total_per_month[x] = agent_total_per_month[x] + all_agent_data[a][x]

    for a in all_agents:
        if a.id not in all_agent_data:
            all_agent_data[a.id] = [str(a), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    all_agent_data[0] = agent_total_per_month

    data = {
        "en_label": en_label,
        "en_total": en_total,
        "en_confirmed": en_confirmed,
        "con_label": client_label,
        "con_data": client_data,
        "agent_label": by_agent_label,
        "agent_data": by_agent_data,
        "all_agent_data": all_agent_data
    }

    return JsonResponse(data)


def segragate_by_client(data_list, by_agent_data):
    for a in data_list:
        if a.agent_id in by_agent_data:
            by_agent_data[a.agent_id][int(a.month)] = a.num
            by_agent_data[a.agent_id][13] = by_agent_data[a.agent_id][13] + a.num
        else:
            by_agent_data[a.agent_id] = [a.agent_name, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            by_agent_data[a.agent_id][int(a.month)] = a.num
            by_agent_data[a.agent_id][13] = by_agent_data[a.agent_id][13] + a.num

    return by_agent_data


def calculate_per_month(data_list, result_list):
    for a in data_list:
        if a.month == "01":
            result_list[0] = a.num
        elif a.month == "02":
            result_list[1] = a.num
        elif a.month == "03":
            result_list[2] = a.num
        elif a.month == "04":
            result_list[3] = a.num
        elif a.month == "05":
            result_list[4] = a.num
        elif a.month == "06":
            result_list[5] = a.num
        elif a.month == "07":
            result_list[6] = a.num
        elif a.month == "08":
            result_list[7] = a.num
        elif a.month == "09":
            result_list[8] = a.num
        elif a.month == "10":
            result_list[9] = a.num
        elif a.month == "11":
            result_list[10] = a.num
        elif a.month == "12":
            result_list[11] = a.num
        else:
            pass


def calculate_client_total(data_list, result_list):
    for a in data_list:
        if a.agent_id == 1:
            result_list[2] = result_list[2] + a.num
        elif a.type == 'fit':
            result_list[1] = result_list[1] + a.num
        elif a.type == 'group':
            result_list[0] = result_list[0] + a.num
        else:
            pass


##
# Only active clients
##
class ClientAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Client.objects.filter(is_archive=0)

        if self.q:
            qs = qs.filter(name__contains=self.q)

        return qs
