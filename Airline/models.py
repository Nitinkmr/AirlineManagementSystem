from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator,validate_email

# Create your models here.


def validate_age(age):
	if age <= 0:
		raise ValidationError(
           _('invalid age'),
           params={'value': age},
    )

def verify_email(email):
	if not validate_email(email):
		raise ValidationError(
           _('invalid email : %(email)s'),
           params={'value': email},
       )

class Passenger(models.Model):
	


	SEX = [("M","Male"),
			("F","Female"),
			("O","Other")]

	FirstName = models.CharField(max_length=30,blank=False)
	LastName = models.CharField(max_length=30,blank=True)
	Sex = models.CharField(max_length=1,choices=SEX,blank=True)
	Age = models.IntegerField(validators=[validate_age],blank=False)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	PhoneNumber = models.CharField(max_length=10,validators=[phone_regex], blank=False) 
	Email = models.CharField(max_length=30,validators=[verify_email],blank=False)
    