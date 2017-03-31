from django.forms import ModelForm
from django import forms
from models import Passenger,Flights
from Airports import get_airports
import datetime

class PassengerForm(ModelForm):

     class Meta:
         model = Passenger
         fields = ['PhoneNumber','Email','FirstName','LastName','Sex','Age']

class SelectFlight(forms.Form):

	Airports = get_airports()
	choices = [(Airport['iata'],Airport['name']) for Airport in Airports]
	FromAirport = forms.ChoiceField(choices)
	ToAirport = forms.ChoiceField(choices)
	Date = forms.DateField(initial=datetime.date.today)
	

class Flights(ModelForm):
	
	class Meta:
		model = Flights
		fields = ['origin','destination','date','flightNum','price','arrivalTime','departureTime']
	