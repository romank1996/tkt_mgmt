from django import forms
from .models import Tickets
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from bootstrap_modal_forms.forms import BSModalModelForm

class TicketForm(forms.ModelForm):
    class Meta:
        model = Tickets
        fields = ["issue_type", "description", "finish_date", "priority"]
        widgets = {
            'finish_date': DatePickerInput(),
        }
        labels={
            "finish_date":"Required Due By",
        }

class ViewTicketForm(BSModalModelForm):
    class Meta:
        model = Tickets
        fields = ['ticket_id', 'issue_type', "description", "finish_date", "priority", 'assigned_to']
