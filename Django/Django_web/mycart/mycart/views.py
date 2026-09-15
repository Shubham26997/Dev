from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
def index(request):
    # pass the name added in the URL patterns and if any dynamic variable added,\
    # then you can add that as well using args=[<variable name>]
    # print(reverse('ShopHome'))
    # print (reverse('ShopContact', args=[details]))

    # return HttpResponse("Welcome on board, Enjoy Shopping or blogging")
    return HttpResponseRedirect(reverse('BlogHome'))