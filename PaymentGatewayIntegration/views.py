from django.shortcuts import render
import requests
from PaymentGatewayIntegration.paypalFile import PayPalClient
from paypalcheckoutsdk.orders import OrdersCreateRequest
from requests.auth import HTTPBasicAuth
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from django.http import JsonResponse


def index(request):
    return render(request,"index.html",{})
@csrf_exempt
def createpaypalorder(request):
    response=CreateOrder().create_order(debug=True)
    return HttpResponse(response)



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

  def create_order(self,debug):
      
    request = OrdersCreateRequest()
    request.prefer('return=representation')
    #3. Call PayPal to set up a transaction
    request.request_body(self.build_request_body())
    response = self.client.execute(request)
    if debug:
      print ('Status Code: ', response.status_code)
      print ('Status: ', response.result.status)
      print ('Order ID: ', response.result.id)
      print ('Intent: ', response.result.intent)
    #   print('Links:'
    #   for link in response.result.links:
    #     print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
    #   print 'Total Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,
    #                      response.result.purchase_units[0].amount.value))

    return response

    """Setting up the JSON request body for creating the order. Set the intent in the
    request body to "CAPTURE" for capture intent flow."""
  @staticmethod
  def build_request_body():
    """Method to create body with CAPTURE intent"""
    return \
      {
        "intent": "CAPTURE",
        "application_context": {
          "brand_name": "EXAMPLE INC",
          "landing_page": "BILLING",
          "shipping_preference": "SET_PROVIDED_ADDRESS",
          "user_action": "CONTINUE"
        },
        "purchase_units": [
          {
            "reference_id": "PUHF",
            "description": "Sporting Goods",

            "custom_id": "CUST-HighFashions",
            "soft_descriptor": "HighFashions",
            "amount": {
              "currency_code": "USD",
              "value": "230.00",
              "breakdown": {
                "item_total": {
                  "currency_code": "USD",
                  "value": "180.00"
                },
                "shipping": {
                  "currency_code": "USD",
                  "value": "30.00"
                },
                "handling": {
                  "currency_code": "USD",
                  "value": "10.00"
                },
                "tax_total": {
                  "currency_code": "USD",
                  "value": "20.00"
                },
                "shipping_discount": {
                  "currency_code": "USD",
                  "value": "10"
                }
              }
            },
            "items": [
              {
                "name": "T-Shirt",
                "description": "Green XL",
                "sku": "sku01",
                "unit_amount": {
                  "currency_code": "USD",
                  "value": "90.00"
                },
                "tax": {
                  "currency_code": "USD",
                  "value": "10.00"
                },
                "quantity": "1",
                "category": "PHYSICAL_GOODS"
              },
              {
                "name": "Shoes",
                "description": "Running, Size 10.5",
                "sku": "sku02",
                "unit_amount": {
                  "currency_code": "USD",
                  "value": "45.00"
                },
                "tax": {
                  "currency_code": "USD",
                  "value": "5.00"
                },
                "quantity": "2",
                "category": "PHYSICAL_GOODS"
              }
            ],
            "shipping": {
              "method": "United States Postal Service",
              "address": {
                "name": {
                  "full_name":"John",
                  "surname":"Doe"
                },
                "address_line_1": "123 Townsend St",
                "address_line_2": "Floor 6",
                "admin_area_2": "San Francisco",
                "admin_area_1": "CA",
                "postal_code": "94107",
                "country_code": "US"
              }
            }
          }
        ]
      }

"""This is the driver function that invokes the createOrder function to create
   a sample order."""
# if __name__ == "__main__":
#   CreateOrder().create_order(debug=True)