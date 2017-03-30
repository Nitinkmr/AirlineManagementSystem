from django.shortcuts import render
from django.http import HttpResponseRedirect
from forms import PassengerForm,FromAndToForm
import json
import requests
import datetime
from django.contrib import messages
from django.contrib.messages import get_messages
# Create your views here.

api_key = "AIzaSyA83nN4Lb-U8ne_uM7Bz0xxAcVEWxNtSfE"
url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=" + api_key
headers = {'content-type': 'application/json'}

def PassengerDetails(request):

	if request.method == 'POST':
		print "post"
		form = PassengerForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
	else:
		print "Get"
		form = PassengerForm()

	return render(request, 'index.html', {'form': form})

def FromAndTo(request):

	if request.method == "POST":
		form = FromAndToForm(request.POST)
		if form.is_valid():			
			data = form.cleaned_data
			FromAirport = data['FromAirport']
			ToAirport = data['ToAirport']
			Date = data['Date']
			print FromAirport

			params = {
			  "request": {
			    "slice": [
			      {
			        "origin": FromAirport,
			        "destination": ToAirport,
			        "date": Date.strftime("%Y-%m-%d")
			      }
			    ],
			    "passengers": {
			      "adultCount": 1
			    },
			    "solutions": 2,
			    "refundable": False
			  }
			}

			response = requests.post(url, data=json.dumps(params), headers=headers)
			data = response.json()
			data = json.dumps(data)
			request.session['flights'] = data
			return HttpResponseRedirect('/airline/displayFlights') 

	else:
		form = FromAndToForm()

	return render(request, 'index.html', {'form': form})

def displayFlights(request):
	
	if 'flights' in request.session:
		flights = request.session.get('flights')
		flights = json.loads(flights)
		flights = flights["trips"]["tripOption"]
		print flights
		result = []
		for flight in flights:
			temp = {
					"rate": flight['saleTotal'],
					"departureTime":flight['slice'][0]['segment'][0]['leg'][0]['departureTime'],
					"arrivalTime":flight['slice'][0]['segment'][0]['leg'][0]['arrivalTime'],
					"duration": flight['slice'][0]['duration']
			}

			result.append(temp)
		print result
		return render(request, 'displayFlights.html', {'flights': result})
	else:
		return render(request, 'displayFlights.html', {'flights': ''})	