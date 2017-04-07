from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import PassengerForm,SelectFlight,getNumPassengers
from .models import Flights,Ticket,Passenger,Booking,IssuedFor
import json
import requests
import datetime
from django.contrib import messages
from django.contrib.messages import get_messages
from django.utils.crypto import get_random_string
# Create your views here.

api_key = "AIzaSyCa1Oko5VirJeqaSpC7GXGeFTU5vBzS5a8"
url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=" + api_key
headers = {'content-type': 'application/json'}
global users 
users = None
def PassengerDetails(request,numPassengers):

	#print request.method
	if request.method == "POST":
		form = PassengerForm(request.POST)
		print "form"
		print form.is_valid()

		if form.is_valid():
			formData = form.cleaned_data
			request.session["phoneNumber"] = formData["PhoneNumber"]
			print formData
			if 'passengerForm' not in request.session:
				request.session["passengerForm"] = []
				users = []
			user = {
					'Email':formData["Email"],
					'PhoneNumber':formData["PhoneNumber"],
					'FirstName':formData["FirstName"],
					'LastName':formData["LastName"],
					'Sex':formData["Sex"],
					'Age':formData["Age"]
					}
			
			global users
			if users == None:
				users = []
			users.append(user)	
			numPassengers = int(numPassengers)
			numPassengers = numPassengers - 1
			
			if numPassengers == 0:
				return HttpResponseRedirect('/airline/displayTicket') 
			else:
				return HttpResponseRedirect('/airline/passengerDetails/' + str(numPassengers))
	
		#	request.session["passengerForm"] = formData
		
		#	return HttpResponseRedirect('/airline/displayTicket') 
	else:
		form = PassengerForm()

	return render(request, 'passengerDetails.html', {'form': form})

def FromAndTo(request):

	if request.method == "POST":
		form = SelectFlight(request.POST)
		print "form"
		print form.is_valid()
		if form.is_valid():			
			data = form.cleaned_data
			FromAirport = data['origin']
			ToAirport = data['destination']
			Date = data['Date']
			 
			try:
				request.session['origin'] = FromAirport
				request.session['destination'] = ToAirport
				request.session['date'] = Date.strftime("%Y-%m-%d")
			except Exception as e:
				print(e)

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
		print flights
		flights = flights["trips"]
		print flights
		if 'tripOption' in flights:
			flights = flights["tripOption"]	
		else:
			print "flights dont exist"			
			return render(request, 'displayFlights.html', {'error': "no flights scheduled fot the given specification",'flights':''})
		
		#print flights
		result = []
		
		for flight in flights:
			temp = {
					"rate": flight['saleTotal'],
					"departureTime":flight['slice'][0]['segment'][0]['leg'][0]['departureTime'],
					"arrivalTime":flight['slice'][0]['segment'][0]['leg'][0]['arrivalTime'],
					"flightNum":flight['slice'][0]['segment'][0]['flight']['number']
			}

			try:
				new_flight = Flights(origin=request.session.get('origin'),destination=request.session.get('destination'),date=request.session.get('date'),flightNum=temp['flightNum'],price=temp['rate'],arrivalTime=temp['arrivalTime'],departureTime = temp['departureTime'])
				new_flight.save()
				result.append(temp)
			except Exception as e:
				print(e)
	return render(request, 'displayFlights.html', {'flights': result})
	
def displaySelectedFlight(request,flightNum):
	#print flightNum
	flight = Flights.objects.all().filter(flightNum=flightNum)
	result = {
				"rate": flight[0].price,
				"departureTime":flight[0].departureTime,
				"arrivalTime":flight[0].arrivalTime,
				"flightNum":flight[0].flightNum		
	}
	request.session['flightNum'] = flightNum
	return render(request, 'displaySelectedFlight.html', {'flight': result})
	
def ticket(request):

	flightNum = request.session.get('flightNum')
	passengerForm = request.session.get('passengerForm')
	flight =  Flights.objects.all().filter(flightNum=flightNum)
	pnr = get_random_string(length=6).upper()
	
	
	try:
		#save ticket#
		newTicket = Ticket(PNR=pnr,price=flight[0].price)
		newTicket.save()

		#save IssuedFor#
	
		form = IssuedFor(PNR=newTicket,flightNum=flight[0])
		form.save()
		#passenger = Passenger.objects.all().filter(PhoneNumber=request.session.get("phoneNumber"))

			#save booking# 
		form = Booking(PNR=newTicket)
		form.save()
		print "users in ticket"	
		print users
		#save passenger#
		for passenger in users:

			age = passenger["Age"]
			sex = passenger["Sex"]
			firstName = passenger["FirstName"]
			lastName = passenger["LastName"]
			phoneNumber = passenger["PhoneNumber"]
			email = passenger["Email"]

			newPassenger = Passenger(Email=email,PhoneNumber=phoneNumber,FirstName=firstName,LastName=lastName,Sex=sex,Age=age,pnrNo=newTicket)	
			newPassenger.save()
		global users	
		users = []
	

		
	except Exception as e:
		print(e)
	return render(request, 'displayTicket.html', {'flightNum': flightNum,'pnr':pnr,'price':flight[0].price})
	
def numPassenger(request):

	if request.method =="POST":
		form = getNumPassengers(request.POST)

		if form.is_valid():
			form = form.cleaned_data
			request.session["numPassengers"] = form["numOfPassengers"]
			return HttpResponseRedirect('/airline/passengerDetails/' + request.session["numPassengers"])
	else:
		form = getNumPassengers()

	return render(request, 'index.html', {'form':form})
	