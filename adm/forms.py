from django import forms
from app.models import Tickets
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput

class TicketForm(forms.ModelForm):
    class Meta:
        model = Tickets
        fields = ["ticket_id","issue_type","created_at", "description", "finish_date","user", "priority","assigned_to"]
        widgets = {
            'finish_date': DatePickerInput(),
        }
        labels={
            "finish_date":"Due By",
            "assigned_to":"Assign To",
        }


class TicketAssignForm(forms.ModelForm):
    class Meta:
        model = Tickets
        fields = ["finish_date", "priority","assigned_to"]
        widgets = {
            'finish_date': DatePickerInput(),
        }
        labels={
            "finish_date":"Due By",
            "assigned_to":"Assign To",
        }


# form for report
import datetime
class ReportForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    date_from = forms.DateTimeField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
    date_to = forms.DateTimeField(initial=datetime.date.today)