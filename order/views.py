from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction

from auth_user_account.serializers import UserSerializer
from menu.serializers import MenuSerializers
from .models import *
from .serializers import *

# Create your views here.


# Order views --path /orders
class OrderListCreateAPIView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
      
        for order_data in serializer.data:
            order = Order.objects.get(id=order_data["id"])
            order_data["account"] = UserSerializer(order.account).data
            order_data["menu_item"] = MenuSerializers(order.menu_item).data

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # handle both single and multiple data
        data = request.data
        print(data)
        if isinstance(data, list):
            # handle multiple data
            serializer = OrderSerializer(data=data, many=True)
        else:
            serializer = OrderSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            msg = (
                "Orders's Successfully"
                if isinstance(data, list)
                else "Order Successfully"
            )

            return Response(
                {"result": serializer.data, "message": msg},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # Delete all items
        try:
            Order.objects.all().delete()
            msg = "All order items deleted successfully"
            return Response({"message": msg}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            msg = "Failed to delete all order items"
            return Response(
                {"messgage": msg, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class OrderDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return None

    def get(self, request, pk):
        order = self.get_object(pk)
        if order is not None:
            serializers = OrderSerializer(order)
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            i_id = int(pk)
            # Check if 'pk' is a valid food ID
            if Order.objects.filter(id=i_id).exists():
                # Update the specific order by setting 'completed' to True
                order = Order.objects.get(id=i_id)
                order.complete = True
                order.save()
                return Response({"message": "Order updated successfully!"})

            return Response(
                {"error": "Invalid  food ID"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, pk):
        order = self.get_object(pk)
        if order is not None:
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


# get order by user id
class OrdersForUser(APIView):
    def get(self, request, pk):
        try:
            orders = Order.objects.filter(account_id=pk)
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        u_id = int(pk)
        try:
            if Order.objects.filter(account_id=u_id).exists():
                orders = Order.objects.filter(account_id=u_id)
                for order in orders:
                    order.complete = True
                    order.save()
                return Response(
                    {"message": "All orders updated successfully!"},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": "Invalid  food ID"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )


class NotCompletedOrder(APIView):
    def get(self, request, pk):
        try:
            orders = Order.objects.filter(account_id=pk, complete=False)
            serializer = OrderSerializer(orders, many=True)
            for order_data in serializer.data:
                order = Order.objects.get(id=order_data["id"])
                order_data["account"] = UserSerializer(order.account).data
                order_data["menu_item"] = MenuSerializers(order.menu_item).data

            return Response({"result": serializer.data}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


#  completed data for the user
class CompletedOrder(APIView):
    def get(self, request, pk):
        try:
            orders = Order.objects.filter(account_id=pk, complete=True)
            serializer = OrderSerializer(orders, many=True)
            for order_data in serializer.data:
                order = Order.objects.get(id=order_data["id"])
                order_data["account"] = UserSerializer(order.account).data
                order_data["menu_item"] = MenuSerializers(order.menu_item).data

            return Response({"result": serializer.data}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# cart views


class CartListCreateAPIView(APIView):
    def calculate_grand_total(self, cart):
        return sum(item.totalPrice for item in cart.f_id.cart_set.all())

    def get(self, request):
        carts = Cart.objects.all()
        serializer = CartSerializer(carts, many=True)
        for cart_data in serializer.data:
            cart = Cart.objects.get(id=cart_data["id"])
            cart_data["u_id"] = UserSerializer(cart.u_id).data
            cart_data["f_id"] = MenuSerializers(cart.f_id).data
            grand_total = self.calculate_grand_total(
                cart
            )  # Calculate grand total for each cart
            cart_data["grand_total"] = grand_total

        return Response({"result": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        # Handle single item order
        serializer = CartSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            msg = "successful"
            return Response(
                {"result": serializer.data, "msg": msg}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # Delete all cart items
        try:
            Cart.objects.all().delete()
            msg = "All cart items deleted successfully"
            return Response({"msg": msg}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            msg = "Failed to delete all cart items"
            return Response(
                {"msg": msg, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CartDetailApiView(APIView):
    def get_object(self, pk):
        try:
            return Cart.objects.get(id=pk)
        except Cart.DoesNotExist:
            return None

    def get(self, request, pk):
        cart = self.get_object(pk)
        if cart is not None:
            serializer = CartSerializer(cart)

            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        pk = int(pk)
        try:
            item = Cart.objects.get(id=pk)
        except Cart.DoesNotExist:
            return Response(
                {"error": "cart not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CartSerializer(instance=item, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"message": "Item updated successfully!", "result": serializer.data}
            )

        return Response(
            {"error": serializer.errors, "message": "Order Update failed."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        cart = self.get_object(pk)
        if cart is not None:
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class CartDataForuser(APIView):
    def get(self, request, pk):
        try:
            cart = Cart.objects.filter(u_id_id=pk)
            serializer = CartSerializer(cart, many=True)

            return Response({"result": serializer.data}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            cart_items = Cart.objects.filter(u_id_id=pk)
            if cart_items.exists():
                cart_items.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
