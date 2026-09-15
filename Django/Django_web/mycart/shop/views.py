from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

# Create your views here.

def index(request):

    # return HttpResponse("Welcome to Shop!!")
    return render(request, "shop/index.html")

def about(request):

    # return HttpResponse("Welcome to About!!")
    return render(request, "shop/about.html")
def contact(request, details=None):
    contact_us = {
        'phone': 7871232726,
        'email': "shubham.goel386@gmail.com",
        'mail_address': "D-401 Ansal Elegance Avantika Extension, GZB"
    }
    if details is None or details not in contact_us:
        # return HttpResponseNotFound("Please pass the required details: [mail_address, phone, email]")
        return HttpResponseNotFound()
    # Using the dynamic URL for getting the required information only instead of providing the whole contact details
    return HttpResponse(f"Welcome to Contact!! with {contact_us[f'{details}']}")
def prodview(request):

    return HttpResponse("Welcome to Prod View!!")
def search(request):

    return HttpResponse("Welcome to Search!!")
def tracker(request):

    return HttpResponse("Welcome to Tracker!!")