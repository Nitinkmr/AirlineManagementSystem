from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
 #   url(r'^$', views.index, name='index'),
    
    url(r'^/?$', views.FromAndTo),
    url(r'^displayFlights?$', views.displayFlights),
    url(r'^numpassenger?$', views.numPassenger),
    
    url(r'^([\w-]+)/$', views.displaySelectedFlight),
    
    url(r'^passengerDetails/([0-9]{1})?$', views.PassengerDetails),
    url(r'^displayTicket?$', views.ticket),
    #url(r'^/?$', views.PassengerDetails),
    url(r'^admin/', admin.site.urls),
       
]