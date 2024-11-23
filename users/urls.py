from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.login, name='login'),
    path('get_states/<int:country_id>/', views.get_states, name='get_states'),
    path('get_cities/<int:state_id>/', views.get_cities, name='get_cities'),
    path('accommodation-form/', views.accommodation_form_view, name='accommodation_form'),
    path('success/', views.success_view, name='success_url'),  # Define a success view and URL
    path('check_email_or_phone/', views.check_email_or_phone, name='check_email_or_phone'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('otpVerification/', views.otpVerification, name='otpVerification'),
    path('check_email_exists/', views.check_email_exists, name='check_email_exists'),
]

