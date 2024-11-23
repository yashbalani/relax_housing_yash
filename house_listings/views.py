from django.shortcuts import render

# Create your views here.
def house_listings(request):
    return render(request, 'house_listings.html')
