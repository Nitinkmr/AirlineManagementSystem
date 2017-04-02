from __future__ import unicode_literals
from django.contrib import admin
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator,validate_email
from random import randint
import datetime
from django.utils.crypto import get_random_string
# Create your models here.


def validate_age(age):
	if age <= 0:
		raise ValidationError(
           _('invalid age'),
           params={'value': age},
    )

def verify_email(email):
	try:
	    validate_email(email)
	except ValidationError as e:
		raise ValidationError(
           _('invalid Email'),
           params={'value': email},
    )
	else:
	    print "hooray! email is valid"
		
	

def verifyPhoneNo(phoneNo):

	condition = (len(phoneNo)<10)

	if len(phoneNo)!= 10:
		raise ValidationError(
           _('invalid Phone Number'),
           params={'value': phoneNo},
    )

def validateName(name):
	try:
	    validate_username(name)
	except ValidationError as e:
		raise ValidationError(
           _('invalid name'),
           params={'value': name},
    )
	else:
	    print "hooray! email is valid"
		


class Passenger(models.Model):
	
	SEX = [("M","Male"),
			("F","Female"),
			("O","Other")]

	Email = models.CharField(max_length=30,blank=False,validators=[verify_email])
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

	'''
	The unique constraint for PhoneNumber is implemented by some checking if a user exists with the provided 
	phone number in our DB.

	'''

	PhoneNumber = models.CharField(max_length=10,validators=[phone_regex],blank=False) 
	
	'''
	add validation to first and last name
	'''
	FirstName = models.CharField(max_length=30,blank=False)
	LastName = models.CharField(max_length=30,blank=True)
	Sex = models.CharField(max_length=1,choices=SEX,blank=True)
	Age = models.IntegerField(validators=[validate_age],blank=False)
	
	

	class Admin: 

	 	pass


class Booking(models.Model):

	PhoneNumber = models.ForeignKey(Passenger)
	PNR = models.CharField(max_length=6,blank=False,default=randint(100000,999999),unique=True)

class Ticket(models.Model):
	PNR =  models.CharField(max_length=6,default=get_random_string(length=6),blank=True)
	price = models.CharField(max_length=10,default=randint(1,1000),blank=False)

class Flights(models.Model):	

	origin = models.CharField(max_length=50,blank=False)
	destination = models.CharField(max_length=50,blank=False)
	date = models.DateField(_("Date"),blank=False)
	flightNum = models.CharField(max_length=50,blank=False,unique=True)
	price = models.CharField(max_length=10,blank=False)
	arrivalTime = models.CharField(max_length=10,blank=False)
	departureTime = models.CharField(max_length=10,blank=False)
	
	class Admin: 

	 	pass

class Aircraft(models.Model):
	modelNo = models.CharField(max_length=15,default="Airbus A320",blank=True)
	capacity = models.IntegerField(blank=True,default=180)
	registrationNumber = models.CharField(max_length=6,default=randint(1000,999999),blank=True,unique=True)

class OperatedBy(models.Model):
	flightNum = models.ForeignKey(Flights)
	registrationNumber = models.ForeignKey(Aircraft)

	class Meta:
		unique_together = (("flightNum","registrationNumber"))

class IssuedFor(models.Model):
	PNR = models.ForeignKey(Ticket,unique=True)
	flightNum = models.ForeignKey(Flights)