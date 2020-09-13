from django import forms
from .models import Tickets
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput

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