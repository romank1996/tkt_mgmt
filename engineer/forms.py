from django import forms
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput

# form for report
import datetime
class ReportFormEng(forms.Form):
    # username = forms.CharField(label="Username", max_length=100)
    date_from = forms.DateTimeField(initial=datetime.date.today().replace(day=1), widget=DatePickerInput(format='%m/%d/%Y'))
    date_to = forms.DateTimeField(initial=datetime.date.today, widget=DatePickerInput(format='%m/%d/%Y'))