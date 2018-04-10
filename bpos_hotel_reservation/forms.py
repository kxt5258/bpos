from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div

from bpos_hotel_reservation.models import HotelReservation, Room, HOTEL_TYPE_CHOICES
from bpos_towns.models import Town
from bpos_status_report.models import Client

from dal import autocomplete


class HotelForm(forms.ModelForm):
    class Meta:
        model = HotelReservation
        fields = '__all__'

    hotel_type = forms.ChoiceField(
        label="Hotel Type",
        choices=HOTEL_TYPE_CHOICES,
        widget=forms.Select(attrs={
            "onChange": 'getFilteredHotels()'}
        )
    )

    town = forms.ModelChoiceField(
        queryset=Town.objects.filter().order_by('id'),
        widget=forms.Select(attrs={
            "onChange": 'getFilteredHotels()'}
        )
    )

    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        widget=autocomplete.ModelSelect2(url='client-autocomplete')
    )

    def clean(self):
        super(HotelForm, self).clean()

    def __init__(self, *args, **kwargs):
        super(HotelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                'client',
                'town',
                'hotel_type',
                'hotel_name',
                'food_option',
                css_class='col-xs-6'
            ),
            Div(
                'arriving_on',
                'leaving_on',
                'notes',
                'is_backup',
                css_class='col-xs-6'
            )
        )


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

    def clean(self):
        super(RoomForm, self).clean()

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                'hotel',
                'room_type',
                'room_category',
                'other_category',
                css_class='col-xs-6'
            ),
            Div(
                'date',
                'quantity',
                'extra_bed',
                'room_status',
                'is_backup',
                css_class='col-xs-6'
            )
        )
