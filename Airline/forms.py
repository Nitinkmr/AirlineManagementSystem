from django.forms import ModelForm
from django import forms
from models import Passenger
from Airports import get_airports
import datetime

class PassengerForm(ModelForm):

     class Meta:
         model = Passenger
         fields = ['FirstName','LastName','Sex','Age','PhoneNumber','Email']

class FromAndToForm(forms.Form):

	Airports = get_airports()
	choices = [(Airport['iata'],Airport['name']) for Airport in Airports]
	FromAirport = forms.ChoiceField(choices)
	ToAirport = forms.ChoiceField(choices)
	Date = forms.DateField(initial=datetime.date.today)
	

	
	