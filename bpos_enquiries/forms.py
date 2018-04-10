from django import forms
from bpos_enquiries.models import Enquiry
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['first_name', 'last_name', 'email', 'phone', 'source', 'planned_trip',
                  'status', 'action_taken', 'other_action', 'is_monitored']

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div('first_name', css_class='col-xs-6'),
                Div('last_name', css_class='col-xs-6')
            ),
            Div(
                Div('email', css_class='col-xs-6'),
                Div('phone', css_class='col-xs-6')
            ),
            Div(
                Div('source', css_class='col-xs-4'),
                Div('planned_trip', css_class='col-xs-4'),
                Div('status', css_class='col-xs-4')
            ),
            Div(
                Div('is_monitored', css_class='col-xs-4'),
                Div('action_taken', css_class='col-xs-4'),
                Div('other_action', css_class='col-xs-4'),
            )
        )
        super(EnquiryForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = super(EnquiryForm, self).clean()
        if not data.get("first_name") and not data.get("last_name"):
            raise forms.ValidationError("Either First Name or Last Name should be entered")

        if not data.get("email") and not data.get("phone"):
            raise forms.ValidationError("Either Phone or Email should be entered")

        if data.get("action_taken") == "other" and not data.get("other_action"):
            raise forms.ValidationError("Other Action is mandatory for Action Taken 'Other'")
