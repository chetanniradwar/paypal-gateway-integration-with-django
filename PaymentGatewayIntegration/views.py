from django.shortcuts import render
import requests
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from django.http import JsonResponse


def index(request):
    return render(request,"index.html",{})
@csrf_exempt
def paypal(request):
    # req1=request.POST[req]
    # res1=request.POST[res]
    if request.method == "POST":
         print("inside post")
         url = "https://api-m.sandbox.paypal.com/v1/payments/payment"
         data={ 
            'user': 'AZS0RdSzskmPsFObSmq1c_C7pLKTuDVZ8jvpczyudM-v57oiDvfcQ3RIfRcsoPpCNLkYW7Ok35cMqgM7',
            'pass': 'EDarMyDvAxfecqAt7ufknBhiIio8nwsIigERY5lFLkGKQfP5aK1K825wpX4i61k8CAka_iUFBjM-a14j',
            'intent': 'sale',
            'payment_method': 'paypal',
            'total': '5.99',
            'currency': 'INR',
            'return_url': 'https://example.com',
            'cancel_url': 'https://example.com'
        }
         response =requests.post(url,data=data)
         print("hi")
        
         print("hello")
         info = response.json()
         print(info)
         return HttpResponse(info)

    
