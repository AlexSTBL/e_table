from django import forms


class DateInput(forms.DateTimeInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class BookForm(forms.Form):
    date = forms.DateField(widget=DateInput)
    time = forms.TimeField(widget=TimeInput)
    number_of_people = forms.IntegerField(max_value=10)
