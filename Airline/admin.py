from django.contrib import admin
from models import Passenger,Flights,Aircraft,OperatedBy,Ticket,Booking,IssuedFor
# Register your models here.
admin.site.register(Passenger)
admin.site.register(Flights)
admin.site.register(Aircraft)
admin.site.register(OperatedBy)
admin.site.register(Ticket)
admin.site.register(Booking)
admin.site.register(IssuedFor)
