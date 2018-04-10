from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from bpos_flights.models import Flight, FlightGroup
from bpos_status_report.models import Member, Client

from dal import autocomplete


class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = '__all__'

    passenger = forms.ModelChoiceField(
        queryset=Member.objects.filter().order_by('id'),
        widget=forms.Select(attrs={
            "onChange": 'getPassengerDetails()'}
        )
    )

    full_name = forms.CharField(
        label="Full Name",
        required=True,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    def clean(self):
        super(FlightForm, self).clean()

    def __init__(self, *args, **kwargs):
        super(FlightForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                'client',
                'passenger',
                'title',
                'full_name',
                'is_student',
                css_class='col-xs-4'
            ),
            Div(
                'dob',
                'fare',
                'other_fare',
                'from_place',
                'to_place',
                css_class='col-xs-4'
            ),
            Div(
                'date',
                'flight_no',
                'flight_class',
                'status',
                'ttl',
                css_class='col-xs-4'
            )
        )


class FlightGroupForm(forms.ModelForm):
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        widget=autocomplete.ModelSelect2(url='client-autocomplete')
    )

    class Meta:
        model = FlightGroup
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FlightGroupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                'client',
                'pax',
                css_class='col-xs-4'
            ),
            Div(
                'comments',
                css_class='col-xs-6'
            )
        )
