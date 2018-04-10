from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div

from bpos_guide_rota.models import GroupGuide, OPTIONS
from bpos_guides.models import Guide
from bpos_status_report.models import Client
from dal import autocomplete


class GuideRotaForm(forms.ModelForm):
    class Meta:
        model = GroupGuide
        fields = ['guide_filter', 'client', 'guide', 'available', 'confirmed', "language", "trek", "confirmed"]

    trek = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    language = forms.CharField(
        label="Specific Language Required",
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    guide_filter = forms.ChoiceField(
        label="Guide Trekking Status",
        choices=OPTIONS,
        widget=forms.Select(attrs={
            "onChange": 'getFilteredGuides()'}
        )
    )

    client = forms.ModelChoiceField(
        queryset=Client.objects.filter().order_by('id'),
        widget=autocomplete.ModelSelect2(url='client-autocomplete',
                                         attrs={
                                             "onChange": 'getClientDetails()'
                                         })
    )

    guide = forms.ModelChoiceField(
        queryset=Guide.objects.filter().order_by('id'),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        if not self.user.has_perm('bpos_guide_rota.change_groupguide_confirmed'):
            pass

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                'client',
                'language',
                'trek',
                css_class='col-md-6'
            ),
            Div(
                'guide_filter',
                'guide',
                'available',
                'confirmed',
                css_class='col-md-6'
            )
        )

        '''if not self.user.has_perm('bpos_guide_rota.change_groupguide_confirmed'):
            self.helper.layout = Layout(
                Div(
                    'client',
                    'language',
                    'trek',
                    css_class='col-md-6'
                ),
                Div(
                    'guide_filter',
                    'guide',
                    'available',
                    css_class='col-md-6'
                )
            ) '''

        super(GuideRotaForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = super(GuideRotaForm, self).clean()
        if not data.get("available") and data.get("confirmed"):
            raise forms.ValidationError("Cannot be confirmed when Unavailable")
