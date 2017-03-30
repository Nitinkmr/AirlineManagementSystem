from django.shortcuts import render
from django.http import HttpResponseRedirect
from forms import PassengerForm,SelectFlight
from models import Flights
import json
import requests
import datetime
from django.contrib import messages
from django.contrib.messages import get_messages
# Create your views here.

api_key = "AIzaSyCa1Oko5VirJeqaSpC7GXGeFTU5vBzS5a8"
url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=" + api_key
headers = {'content-type': 'application/json'}

def PassengerDetails(request):

	if request.method == 'POST':
		form = PassengerForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
	else:
		form = PassengerForm()

	return render(request, 'index.html', {'form': form})

def FromAndTo(request):

	if request.method == "POST":
		print "Post"
		form = SelectFlight(request.POST)
		if form.is_valid():			
			data = form.cleaned_data
			FromAirport = data['FromAirport']
			ToAirport = data['ToAirport']
			Date = data['Date']
			 

		
			try:
				request.session['origin'] = FromAirport
				request.session['destination'] = ToAirport
				request.session['date'] = Date.strftime("%Y-%m-%d")
			except Exception as e:
				print e

			return HttpResponseRedirect('/airline/displayFlights') 

	else:
		form = SelectFlight()

	return render(request, 'index.html', {'form': form})

def displayFlights(request):
	
	'''
	if required flight is in DB, show from there only, else proceed as follows
	'''
	origin = request.session.get('origin')
	destination = request.session.get('destination')
	date = request.session.get('date')

	flights = Flights.objects.all().filter(origin=origin,destination=destination,date=date)
	if len(flights)>0:
		print "flights from DB"
		result = []
		for flight in flights:
			temp = {
					"rate": flight.price,
					"departureTime":flight.departureTime,
					"arrivalTime":flight.arrivalTime,
					"flightNum":flight.flightNum
			}

			result.append(temp)
	else:
		params = {
			  "request": {
			    "slice": [
			      {
			        "origin": origin,
			        "destination": destination,
			        "date": date
			      }
			    ],
			    "passengers": {
			      "adultCount": 1
			    },
			    "solutions": 20,
			    "refundable": False
			  }
			}
	
		response = requests.post(url, data=json.dumps(params), headers=headers)
		data = response.json()
		data = json.dumps(data)
		
		flights = data
		flights = json.loads(flights)
		flights = flights["trips"]["tripOption"]
		#print flights
		result = []
		origin = str(origin)
		print origin
		for flight in flights:
			temp = {
					"rate": flight['saleTotal'],
					"departureTime":flight['slice'][0]['segment'][0]['leg'][0]['departureTime'],
					"arrivalTime":flight['slice'][0]['segment'][0]['leg'][0]['arrivalTime'],
					"flightNum":flight['slice'][0]['segment'][0]['flight']['number']
			}

			new_flight = Flights(origin=request.session.get('origin'),destination=request.session.get('destination'),date=request.session.get('date'),flightNum=temp['flightNum'],price=temp['rate'],arrivalTime=temp['arrivalTime'],departureTime = temp['departureTime'])
			new_flight.save()
			result.append(temp)
		
		print result
	return render(request, 'displayFlights.html', {'flights': result})
	