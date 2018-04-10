from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, Button, Submit
from crispy_forms.bootstrap import FormActions
from bpos_payments.models import Payment, PayExtraItem, PayPaymentOut

from dal import autocomplete


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = '__all__'
        widgets = {
            'client': autocomplete.ModelSelect2(url='client-autocomplete')
        }

    def clean(self):
        super(PaymentForm, self).clean()

    def __init__(self, *args, **kwargs):
        label = kwargs.pop('label')
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Fieldset(
                    'Tour Price',
                    'client',
                    'tour',
                    'flight',
                    'flight_estimated',
                    'visa',
                    'bank',
                    css_class='col-xs-6')
            ),
            Div(
                Fieldset(
                    'Payment',
                    'deposit',
                    'balance',
                    'payment',
                    'la_date',
                    'bank_form',
                    'amount_received',
                ),
                Fieldset(
                    'Money To Pay and Collect',
                    'money_owed',
                    'amount',
                    'paid',
                    'collected',
                ),
                Fieldset(
                    'Cancellation',
                    'group_cancelled',
                    'member_cancelled',
                    'refund',
                ),
                css_class='col-xs-6'
            ),
            Div(
                Div(
                    FormActions(
                        Submit('submit_form', label, css_class='btn btn-success'),
                        Button('cancel_form', 'Cancel', css_class='btn btn-info', onclick="window.history.back();"),
                        css_class='col-xs-3'
                    )
                ),
                css_class='col-xs-12'
            )
        )


class ExtraItemForm(forms.ModelForm):
    class Meta:
        model = PayExtraItem
        fields = '__all__'

    def clean(self):
        super(ExtraItemForm, self).clean()

    def __init__(self, *args, **kwargs):
        super(ExtraItemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                'client',
                css_class='col-xs-4'
            ),
            Div(
                'item',
                css_class='col-xs-4'
            ),
            Div(
                'amount',
                css_class='col-xs-4'
            ),
        )


class PaymentOutsForm(forms.ModelForm):
    class Meta:
        model = PayPaymentOut
        fields = '__all__'

    def clean(self):
        super(PaymentOutsForm, self).clean()

    def __init__(self, *args, **kwargs):
        super(PaymentOutsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                'client',
                css_class='col-xs-3'
            ),
            Div(
                'item',
                css_class='col-xs-3'
            ),
            Div(
                'amount',
                css_class='col-xs-3'
            ),
            Div(
                'paid',
                css_class='col-xs-3'
            ),
        )
