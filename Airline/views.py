from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import PassengerForm,SelectFlight,getNumPassengers
from .models import Flights,Ticket,Passenger,Booking,IssuedFor,Aircraft,OperatedBy
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
		
		

		if form.is_valid():
			formData = form.cleaned_data
			request.session["phoneNumber"] = formData["PhoneNumber"]
		
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
		
	
		if form.is_valid():			
			data = form.cleaned_data
			FromAirport = data['origin']
			ToAirport = data['destination']
			Date = data['Date']

			if FromAirport==ToAirport:
				return render(request, 'displayFlights.html', {'form': '','error':'Origin and Destination can\'t be same'})
			 
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
			    "solutions": 1,
			    "refundable": False
			  }
			}
	
		response = requests.post(url, data=json.dumps(params), headers=headers)
		data = response.json()
		data = json.dumps(data)
		


		flights = data
		flights = json.loads(flights)
		
		flights = flights["trips"]
		
		if 'tripOption' in flights:
			flights = flights["tripOption"]	
		else:
			print "flights dont exist"			
			return render(request, 'displayFlights.html', {'error': "no flights scheduled fot the given specification",'flights':''})
		


		#print flights
		result = []
		aircrafts = Aircraft.objects.all()
		x = 0
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
				
				form = OperatedBy(flightNum=new_flight,registrationNumber=aircrafts[x],dt=new_flight)
				form.save()
				x = x+1
			except Exception as e:
				print(e)
	
	return render(request, 'displayFlights.html', {'flights': result})
	
def displaySelectedFlight(request,flightNum):
	#print flightNum
	flight = Flights.objects.all().filter(flightNum=flightNum,date=request.session.get('date'))
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
	flight =  Flights.objects.all().filter(flightNum=flightNum,date=request.session.get('date'))
	print flight[0].flightNum
	print flight[0].seatsAvailable
	
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

		
		#flight[0].seatsAvailable = int(flight[0].seatsAvailable)-int(len(users))
		flight.update(seatsAvailable = int(flight[0].seatsAvailable)-int(len(users)))
		#flight[0].save()
		#flight =  Flights.objects.all().filter(flightNum=flightNum,date=request.session.get('date'))
		print flight[0].flightNum
		print flight[0].seatsAvailable
	
		
		global users	
		users = []
	

		
	except Exception as e:
		print(e)
	return render(request, 'displayTicket.html', {'flightNum': flightNum,'pnr':pnr,'price':flight[0].price})
	
def numPassenger(request):

	if request.method =="POST":
		form = getNumPassengers(request.POST)
		flightNum = request.session.get('flightNum')

		flight = Flights.objects.all().filter(flightNum=flightNum,date=request.session.get('date'))
		
		seatsAvailable = flight[0].seatsAvailable
		
		if form.is_valid():
			form = form.cleaned_data
			request.session["numPassengers"] = form["numOfPassengers"]
			
			if int(seatsAvailable) == 0 or int(form["numOfPassengers"])>int(seatsAvailable):
				return render(request, 'displayFlights.html', {'form':'','error':'required number of seats not available'})
		

			return HttpResponseRedirect('/airline/passengerDetails/' + request.session["numPassengers"])
	else:
		form = getNumPassengers()

	return render(request, 'index.html', {'form':form})
	