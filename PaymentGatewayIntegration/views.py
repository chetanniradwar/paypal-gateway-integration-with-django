from django.shortcuts import render
import requests
from PaymentGatewayIntegration.paypalFile import PayPalClient
from paypalhttp.serializers.json_serializer import Json
from paypalcheckoutsdk.orders import OrdersCreateRequest
from paypalcheckoutsdk.orders import OrdersGetRequest

from requests.auth import HTTPBasicAuth
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from django.http import JsonResponse
import json

orderid=""
def index(request):
    return render(request,"index.html",{})
@csrf_exempt
def createpaypalorder(request):
    print("i am at cretatepaypalorder")
    Responsee=CreateOrder().create_order(debug=True)
    # print(json.dumps(response))
    print(Responsee)
    print(type(Responsee))
    # print(Responsee.result)
    # print(type(Responsee.result))
    # Responsee=Responsee.json()
    return JsonResponse(Responsee)
@csrf_exempt
def getpaypaltransactiondetails():
    print("i am at getpaytpaltransactiondetails")
    order=GetOrder().get_order(orderid)

    return HttpResponse(order)

    # req1=request.POST[req]
    # res1=request.POST[res]

    # if request.method == "POST":
    #      print("inside post")
    #      auth_url="https://api-m.sandbox.paypal.com/v2/oauth2/token"
    #      auth_header={'Accept': 'application/json','Accept-Language': 'en_US'}
    #      auth_response= requests.post(auth_url,headers=auth_header, auth=('AZS0RdSzskmPsFObSmq1c_C7pLKTuDVZ8jvpczyudM-v57oiDvfcQ3RIfRcsoPpCNLkYW7Ok35cMqgM7','EDarMyDvAxfecqAt7ufknBhiIio8nwsIigERY5lFLkGKQfP5aK1K825wpX4i61k8CAka_iUFBjM-a14j'),data={'grant_type':'client_credentials'})
    #      print(auth_response.json())
    #      auth_res=auth_response.json()
    #      print(type(auth_res))
    #      access_token=auth_res['access_token']
    #      appid=auth_res['app_id']
    #      print( access_token)
    #      print(appid)
    #      url = "https://api-m.sandbox.paypal.com/v1/payments/payment"
    #      header={
    #          'Content-Type': 'application/json',
    #          'Authorization':'Bearer ' + access_token
    #      }
    #      data={ 
    #         'auth':
    #         {
    #             'user': 'AZS0RdSzskmPsFObSmq1c_C7pLKTuDVZ8jvpczyudM-v57oiDvfcQ3RIfRcsoPpCNLkYW7Ok35cMqgM7',
    #             'pass': 'EDarMyDvAxfecqAt7ufknBhiIio8nwsIigERY5lFLkGKQfP5aK1K825wpX4i61k8CAka_iUFBjM-a14j'
    #         },
    #         'body':
    #         {
    #             'intent': 'sale',
    #             'payer':
    #             {
    #                 'payment_method': 'paypal'
    #             },
    #             'transactions': [
    #                 {
    #                     'amount':
    #                     { 
    #                         'total': '5.99',
    #                         'currency': 'USD'
    #                     }
    #                 }],
    #             'redirect_urls':
    #             { 
    #                 'return_url': 'http:http://127.0.0.1:8000/',
    #                 'cancel_url': 'http:http://127.0.0.1:8000/'
    #             }
           
    #         },
    #         'json':'True'
    #     }
    #      response =requests.post(url,headers=header,json=data)
    #      print("hi")
        
    #      print("hello")
    #      info = response.json()
    #      print(info)
    #      return HttpResponse(info)




# 1. Import the PayPal SDK client that was created in `Set up Server-Side SDK`.

class CreateOrder(PayPalClient):

  #2. Set up your server to receive a call from the client
  """ This is the sample function to create an order. It uses the
    JSON body returned by buildRequestBody() to create an order."""

  def create_order(self,debug=True):
      
    request = OrdersCreateRequest()
    request.headers['prefer'] = 'return=representation'
   
    #3. Call PayPal to set up a transaction
    request.request_body(
      {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": "100.00"
                }
            }
        ]
    }
    )
    response = self.client.execute(request)
    if debug:
      print ('Status Code: ', response.status_code)
      print ('Status: ', response.result.status)
      orderid=response.result.id
      print(type(orderid))
      print ('Order ID: ', response.result.id)
      print ('Intent: ', response.result.intent)
      for link in response.result.links:
        print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
        print('Total Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,
                         response.result.purchase_units[0].amount.value))
    print(response)
    print(type(response))
    print(response.result)
    print(type(response.result))
    # print(json.dumps(response))
    # hi=json.dumps(response)
    json_data = self.object_to_json(response.result)
    print("json_data: ", json.dumps(json_data,indent=4))
    return json_data
    # return response.result

# if __name__ == "__main__":
#   CreateOrder().create_order(debug=True)


# 1. Import the PayPal SDK client that was created in `Set up Server-Side SDK`.
# from sample import PayPalClient

class GetOrder(PayPalClient):

  #2. Set up your server to receive a call from the client
  """You can use this function to retrieve an order by passing order ID as an argument"""   
  def get_order(self, order_id):
    """Method to get order"""
    request = OrdersGetRequest(order_id)
    #3. Call PayPal to get the transaction
    response = self.client.execute(request)
    #4. Save the transaction in your database. Implement logic to save transaction to your database for future reference.
    print ('Status Code: ', response.status_code)
    print ('Status: ', response.result.status)
    print ('Order ID: ', response.result.id)
    print ('Intent: ', response.result.intent)
    # print ('Links:'
    # for link in response.result.links:
    #   print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
    # print 'Gross Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,
    #                    response.result.purchase_units[0].amount.value)

"""This driver function invokes the get_order function with
   order ID to retrieve sample order details. """
# if __name__ == '__main__':
  # GetOrder().get_order('REPLACE-WITH-VALID-ORDER-ID')