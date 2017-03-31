from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
 #   url(r'^$', views.index, name='index'),
    
    url(r'^/?$', views.FromAndTo),
    url(r'^displayFlights?$', views.displayFlights),
    url(r'^([0-9]{3})/$', views.displaySelectedFlight),
    
    #url(r'^/?$', views.PassengerDetails),
    url(r'^admin/', admin.site.urls),
       
]