from django.shortcuts import render
import requests
from PaymentGatewayIntegration.paypalFile import PayPalClient
from paypalhttp.serializers.json_serializer import Json
from paypalcheckoutsdk.orders import OrdersCreateRequest
from paypalcheckoutsdk.orders import OrdersCaptureRequest
from paypalcheckoutsdk.orders import OrdersGetRequest

from requests.auth import HTTPBasicAuth
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from django.http import JsonResponse
import json

from .models import donor
from .models import transaction

orderid=""
def onformsubmit(request):
  first_name=request.GET['firstName']
  last_name=request.GET['lastName']
  email_id=request.GET['emailAdd']
  mobile_no=request.GET['mobile']
  amount=request.GET['amount']
  request.session.get('amount',0)
  request.session['amount']=amount
  current_donor=donor.objects.create(email_id=email_id, first_name=first_name,last_name=last_name,mobile_no=mobile_no)
  request.session.get('current_donor',None)
  request.session['current_donor']=current_donor.id
  return render(request,'paymentoption.html',{'firstName':first_name,'lastName':last_name})


def index(request):
    return render(request,"index.html",{})
@csrf_exempt
def createpaypalorder(request):
    print("i am at cretatepaypalorder")
    amt=request.session.get('amount')
    curr_donor=request.session.get('current_donor')
    Responsee=CreateOrder().create_order(debug=True,amt_value=amt,present_donor=curr_donor)

    return JsonResponse(Responsee)
@csrf_exempt
def getpaypaltransactiondetails(request):
    print("i am at getpaytpaltransactiondetails")
    order=GetOrder().get_order(orderid)
    return JsonResponse(order)

@csrf_exempt 
def capturepaypalorder(request):
    data=json.loads(request.body.decode("utf-8"))
    
    print(data)
    ordrid=data['orderID']
    curr_donor=request.session.get('current_donor')
    capture=CaptureOrder().capture_order(ordrid,debug=True,present_donor=curr_donor)
    return JsonResponse(capture)


def getsuccesspage(request):
    return render(request,'success.html') 

def getfailurepage(request):
    return render(request,'failure.html')   
# 1. Import the PayPal SDK client that was created in `Set up Server-Side SDK`.



class CreateOrder(PayPalClient):

  #2. Set up your server to receive a call from the client
  """ This is the sample function to create an order. It uses the
    JSON body returned by buildRequestBody() to create an order."""

  def create_order(self,debug=True,amt_value=0,present_donor=None):
      
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
                    "value": amt_value
                }
            }
        ]
    }
    )
    response = self.client.execute(request)
    orderid=response.result.id
    print('first=='+orderid)
    if debug:
      print ('Status Code: ', response.status_code)
      print ('Status: ', response.result.status)
      
      print ('Order ID: ', response.result.id)
      print ('Intent: ', response.result.intent)
      for link in response.result.links:
        print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
        print('Total Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,
                         response.result.purchase_units[0].amount.value))
    foreign_key=donor.objects.get(id=present_donor)
    transaction.objects.create(donor=foreign_key,order_id=response.result.id,amount_val=amt_value,status=response.result.status)
    print(response)
    print(type(response))
    print(response.result)
    print(type(response.result))
    # print(json.dumps(response))
    # hi=json.dumps(response)
    json_data = self.object_to_json(response.result)
    print("create_order_json_data: ", json.dumps(json_data,indent=4))
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
    print('Links :')
    for link in response.result.links:
      print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
    print('Gross Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,
                       response.result.purchase_units[0].amount.value))
 
    json_data = self.object_to_json(response.result)
    print("get_order_json_data: ", json.dumps(json_data,indent=4))
    return json_data
"""This driver function invokes the get_order function with
   order ID to retrieve sample order details. """
# if __name__ == '__main__':
  # GetOrder().get_order('REPLACE-WITH-VALID-ORDER-ID')




  
class CaptureOrder(PayPalClient):
        
    """this is the sample function performing payment capture on the order. Approved Order id should be passed as an argument to this function"""

    def capture_order(self, order_id, debug=True,present_donor=None):
        """Method to capture order using order_id"""
        print('order_id==='+order_id)
        request = OrdersCaptureRequest(order_id)
        response = self.client.execute(request)
        if debug:
            print ('Status Code: ', response.status_code)
            print ('Status: ', response.result.status)
            print ('Order ID: ', response.result.id)
            print ('Links: ')
            for link in response.result.links:
                print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
            print ('Capture Ids: ')
            for purchase_unit in response.result.purchase_units:
                for capture in purchase_unit.payments.captures:
                    print('\t', capture.id)
                    captureId=capture.id
            try:

              print ("Buyer:")
              print ("\tEmail Address: {}\n\tName: {}\n\tPhone Number:".format(response.result.payer.email_address,
                                                                            response.result.payer.name.given_name + " " + response.result.payer.name.surname))
                                                                          #  response.result.payer.phone.phone_number.national_number))
            except:
              print("error")
            json_data = self.object_to_json(response.result)
            print ("capture_json_data: ", json.dumps(json_data,indent=4))
            curr_tran=transaction.objects.get(id=present_donor)
            curr_tran.capture_id=captureId
            curr_tran.status=response.result.status
            curr_tran.save()
            
        return json_data


"""This is the driver function which invokes the capture order function. Order Id value should be replaced with the approved order id. """
# if __name__ == "__main__":
    # order_id = '8G344453R30787301'
    # CaptureOrder().capture_order(order_id, debug=True)