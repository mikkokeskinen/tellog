from django import forms


class CustomDateInput(forms.DateInput):
    input_type = 'date'


class SearchForm(forms.Form):
    q = forms.CharField(label='Search', required=False)
    username = forms.CharField(label='Username', required=False)
    date = forms.DateField(label='Date', required=False,
                           widget=CustomDateInput)
