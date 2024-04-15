import json
import uuid
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect, render
from order.models import Order
class GenerateUUID(APIView):
    def get(self, request):
        id = uuid.uuid4()
        print(id)
        return Response({'uuid': id})

class InitKhaltiAPIView(APIView):
    def post(self, request):
        url = "https://a.khalti.com/api/v2/epayment/initiate/"
        return_url = request.data.get('return_url')
        amount = request.data.get('amount')
        purchase_order_id = request.data.get('purchase_order_id')

        payload = json.dumps({
            "return_url": return_url,
            "website_url": 'http://localhost:3000/',
            "amount": amount,
            "purchase_order_id": purchase_order_id,
            "purchase_order_name": "test",
            "customer_info": {
                "name": "Bibek Dahal",
                "email": "test@khalti.com",
                "phone": "9800000001"
            }
        })

        headers = {
            'Authorization': 'key 996240dbe58b428d979ba03f5a0ebdb6',
            'Content-Type': 'application/json',
        }

        response = requests.post(url, headers=headers, data=payload)
        new_res = json.loads(response.text)
        return Response({'payment_url': new_res['payment_url']})
        

class VerifyKhaltiAPIView(APIView):
    def get(self, request):
        url = "https://a.khalti.com/api/v2/epayment/lookup/"
        headers = {
            'Authorization': 'key 996240dbe58b428d979ba03f5a0ebdb6',
            'Content-Type': 'application/json',
        }
        pidx = request.query_params.get('pidx')
        print('id',pidx)
        data = json.dumps({'pidx': pidx})
        res = requests.post(url, headers=headers, data=data)
        new_res = json.loads(res.text)
        print(new_res)

        if new_res['status'] == 'Completed':
            # Perform your logic for a completed payment
            # order_id = new_res['order_id']

            # # Retrieve the order
            # order = Order.objects.get(pk=order_id)
            
            # # Update the 'paid' field of the order to True
            # order.paid = True
            # order.save()
            pass
        
        return redirect('http://localhost:3000/dashboard/user/myorder')

    
