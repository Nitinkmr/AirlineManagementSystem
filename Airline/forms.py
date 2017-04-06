from django.forms import ModelForm
from django import forms
from .models import Passenger,Flights
from .Airports import get_airports
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.forms.extras.widgets import SelectDateWidget
import datetime

def validateDate(datePassed):

	if (datePassed.month >= (datetime.date.today().month+6)) :
		raise forms.ValidationError("Bookings can not be done for dates 6 months beyind the current date")


	if (datePassed<datetime.date.today()):
		raise forms.ValidationError("Invalid date")

class PassengerForm(ModelForm):

     class Meta:
         model = Passenger
         fields = ['PhoneNumber','Email','FirstName','LastName','Sex','Age']

class SelectFlight(forms.Form):

	Airports = get_airports()
	choices = [(Airport['iata'],Airport['name']) for Airport in Airports]
	
	origin = forms.ChoiceField(choices)
	destination = forms.ChoiceField(choices)
	Date = forms.DateField(initial=datetime.date.today,validators=[validateDate],widget=SelectDateWidget)
	

class Flights(ModelForm):
	
	class Meta:
		model = Flights
		fields = ['origin','destination','date','flightNum','price','arrivalTime','departureTime']
	
