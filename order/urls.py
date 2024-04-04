from django.urls import path
from .views import *
urlpatterns = [
    path('orders/',OrderListCreateAPIView.as_view(), name="Order-list-create" ),
    path("orders/<int:pk>/", OrderDetailAPIView.as_view(), name="single order item"),
    path("orders/user/<int:pk>/", OrdersForUser.as_view(), name="users orders"),
    path('not-completed-orders/<int:pk>/', NotCompletedOrder.as_view(), name='not-completed-order'),
    path('completed-orders/<int:pk>/', CompletedOrder.as_view(), name='completed-order'),
    path('cart/',CartListCreateAPIView.as_view(), name="cart-list"),
    path('cart/<int:pk>/', CartDetailApiView.as_view(), name='cart-detail'),
    path('carts/<int:pk>/', CartDataForuser.as_view(), name='cart-detail'),

]
