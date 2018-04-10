from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Button, Submit
from crispy_forms.bootstrap import FormActions

from bpos_status_report.models import Client, Member, Document


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ['payment_status', 'hotel_status', 'visa_status', 'flight_status', 'name', 'guide_notified']

    def clean(self):
        data = super(ClientForm, self).clean()
        if not data.get("agent") and not data.get("type") and not data.get('group_name'):
            raise forms.ValidationError("Agent, Type, and Group Name are mandatory")

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                'agent',
                'type',
                'group_name',
                'pax',
                'language_guide_needed',
                'language',
                'other_language',
                css_class='col-xs-6'
            ),
            Div(
                'arriving_date',
                'leaving_date',
                'entering_from',
                'leaving_to',
                'trek',
                'other_trek',
                css_class='col-xs-6'
            )
        )


class ClientEditForm(ClientForm):
    class Meta(ClientForm.Meta):
        exclude = ['name', 'agent']

    def clean(self):
        super(ClientEditForm, self).clean()

    def __init__(self, *args, **kwargs):
        super(ClientEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                'type',
                'group_name',
                'pax',
                'arriving_date',
                'leaving_date',
                'entering_from',
                'leaving_to',
                'trek',
                'other_trek',
                css_class='col-xs-6'
            ),
            Div(
                'flight_status',
                'payment_status',
                'hotel_status',
                'visa_status',
                'guide',
                'guide_notified',
                'language_guide_needed',
                'language',
                'other_language',
                css_class='col-xs-6'
            )
        )


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    'client',
                    css_class='col-xs-4'
                ),
                Div(
                    'title',
                    css_class='col-xs-4'
                ),
                Div(
                    'full_name',
                    css_class='col-xs-4'
                ),
                css_class='col-xs-12'
            ),
            Div(
                Div(
                    'is_student',
                    css_class='col-xs-4'
                ),
                css_class='col-xs-8'
            )
        )


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        label = kwargs.pop('label')
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    'client',
                    'document_for',
                    'document_type',
                    css_class='col-xs-4'
                ),
                Div(
                    'document',
                    'visa_alert',
                    'ticket_alert',
                    css_class='col-xs-4'
                ),
                Div(
                    'comment',
                    css_class='col-xs-4'
                ),
                css_class='col-xs-12'
            ),
            Div(
                Div(
                    FormActions(
                        Submit('submit_form', label, css_class='btn btn-success'),
                        Button('cancel_form', 'Cancel', css_class='btn btn-info', onclick="window.history.back();")
                    ),
                    css_class='col-xs-6'
                ),
                css_class='col-xs-12'
            )
        )
