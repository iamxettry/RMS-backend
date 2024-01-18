from django.urls import path
from .views import RegisterView,UserLoginView,SendPasswordResetEmailView,UserPasswordResetView,UserProfileView
urlpatterns = [
    path('signup/',RegisterView.as_view(), name='register'),
    path('login/',UserLoginView.as_view(), name='login'),
    path('profile/',UserProfileView.as_view(), name='profile'),

    path('request-password-reset/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),

]