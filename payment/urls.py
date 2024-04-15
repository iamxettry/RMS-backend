from django.urls import path
from .views import *
urlpatterns = [
    path('uuid/', GenerateUUID.as_view(), name="get-uuid"),
    path('initiate/', InitKhaltiAPIView.as_view(), name="payment-initiate"),
    path('verify/',VerifyKhaltiAPIView.as_view(),name="verify")
  

]