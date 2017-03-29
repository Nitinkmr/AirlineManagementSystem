from django.shortcuts import render
from forms import PassengerForm

# Create your views here.

def PassengerDetails(request):

	if request.method == 'POST':
		print "post"
		form = PassengerForm(request.POST)
	else:
		print "Get"
		form = PassengerForm()

	return render(request, 'index.html', {'form': form})
