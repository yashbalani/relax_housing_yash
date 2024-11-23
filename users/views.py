import json
from users.models import AdditionalPreferenceModel, InterestModel, LifestylePreferenceModel, MinLengthOfStayModel, PurposeOfStayModel, RoomPreferenceModel, UserAccommodationInfoModel, UserLocationDetailsModel, UserModel
from location.models import CountriesDialCodeModel, CountriesModel, StatesModel, CitiesModel
from django.shortcuts import render
from .forms import UserSignUpForm
from django.contrib import messages
import random
import string
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

def homepage(request):
    return render(request, 'homepage.html')

def verify_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email_otp_input = data.get('email_otp')
        phone_otp_input = data.get('phone_otp')

        # Retrieve stored OTPs from session
        stored_email_otp = request.session.get('email_otp')
        stored_phone_otp = request.session.get('phone_otp')

        if email_otp_input == stored_email_otp and phone_otp_input == stored_phone_otp:
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid OTPs.'})
        
# Function to generate a random OTP
def generate_otp():
    otp = ''.join(random.choices(string.digits, k=6))  # 6-digit OTP
    return otp

# Function to send OTP via email
def send_email_otp(email, otp):
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp}'
    print("otp")
    print(otp)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

# Simulated function to send OTP to phone (console/log for testing purposes)
def send_phone_otp(phone_number, otp):
    print(f"Simulated OTP for phone {phone_number}: {otp}")

def check_email_or_phone(request):
    email = request.GET.get('email', None)
    phone_number = request.GET.get('phone_number', None)

    # Check if email exists in the database
    if email and UserModel.objects.filter(email_address=email).exists():
        return JsonResponse({'exists': True, 'message': 'This email address is already in use. Please login.'})
    # Check if phone number exists in the database
    if phone_number and UserModel.objects.filter(phone_number=phone_number).exists():
        return JsonResponse({'exists': True, 'message': 'This phone number is already in use. Please login.'})
    print(phone_number)
    return JsonResponse({'exists': False})

def otpVerification(request):
    if request.method == 'POST':
    
        email = request.POST.get('email_address')
        phone_number = request.POST.get('phone_number')

        # Generate OTPs
        email_otp = generate_otp()
        phone_otp = generate_otp()

        # Send OTPs
        send_email_otp(email, email_otp)
        send_phone_otp(phone_number, phone_otp)

        # Store OTPs temporarily in session for verification
        request.session['email_otp'] = email_otp
        request.session['phone_otp'] = phone_otp

        # Send OTPs and show alert to user
        return JsonResponse({'status': 'success', 'message': 'OTPs sent! Please check your email and phone for the OTPs.'})

def login(request):
    return render(request, 'login.html')

@csrf_exempt
def check_email_exists(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        # Check if email exists in the database
        try:
            user = UserModel.objects.get(email_address=email,password=password)
            # Authenticate the user with the provided password
            if user is not None:
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid email or password.'})
        except UserModel.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Email not registered.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def user_signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST, request.FILES)
        print("formvalid")
        print(form.is_valid())
        print(form.cleaned_data) 

        if form.is_valid():
            user = form.save()
            
            # Get the location details from the form
            country_id = form.cleaned_data["country"]
            state_id = form.cleaned_data['state']
            city_id = form.cleaned_data['city']

            # Create a UserLocationDetailsModel instance
            location_details = UserLocationDetailsModel(
                user=user,
                country_id=country_id,
                state_id=state_id,
                city_id=city_id,
                is_active=True  # Or whatever condition you want to set
            )
            location_details.save()
            return JsonResponse({'status': 'success'})
        else:
            # Print the form errors to understand why it's invalid
            print(form.errors)
            return JsonResponse({'status': 'error', 'message': 'Form is invalid'})
    else:
        form = UserSignUpForm()
    interests = InterestModel.objects.all()
    countries = CountriesModel.objects.all()
    country_codes = CountriesDialCodeModel.objects.all()
    return render(request, 'signup.html', {'form': form, 'interests': interests, 'countries': countries,'country_codes':country_codes})

# Fetch states for a given country
def get_states(request, country_id):
    print(country_id)
    states = StatesModel.objects.filter(country_id=country_id).values('state_id', 'state_name')
    return JsonResponse({'states': list(states)})

# Fetch cities for a given state
def get_cities(request, state_id):
    cities = CitiesModel.objects.filter(state_id=state_id).values('id', 'name')
    return JsonResponse({'cities': list(cities)})

# Main page view
def index(request):
    # Fetch all countries from the database to pass to the template
    countries = CountriesModel.objects.all()  # Or use a related model for countries if applicable
    room_preferences = RoomPreferenceModel.objects.all()
    lifestyle_preferences = LifestylePreferenceModel.objects.all()
    interests = InterestModel.objects.all()
    additional_preferences = AdditionalPreferenceModel.objects.all()
    min_length_of_stay = MinLengthOfStayModel.objects.all()
    purpose_of_stay = PurposeOfStayModel.objects.all()

    # Pass the data to the template context
    context = {
        'countries': countries,
        'room_preferences': room_preferences,
        'lifestyle_preferences': lifestyle_preferences,
        'interests': interests,
        'additional_preferences': additional_preferences,
        'min_length_of_stay' : min_length_of_stay,
        'purpose_of_stay' : purpose_of_stay
    }
    return render(request, 'base.html', context)

def accommodation_form_view(request):
    if request.method == 'POST':
        user_form = UserSignUpForm(request.POST, request.FILES)
        accommodation_form = UserAccommodationInfoModel(request.POST)
        
        if user_form.is_valid() and accommodation_form.is_valid():
            # Save the user data
            email = request.POST.get('email_address')
            
            # Check if the email already exists in the database
            if UserModel.objects.filter(email_address=email).exists():
                print("svsvsdvsdv")
                # Send a message to the template if email exists
                messages.error(request, "This email address is already registered in our database.")
                return render(request, 'index.html')
            
            user_instance = user_form.save()
            
            # Link the user to the accommodation info and save
            accommodation_instance = accommodation_form.save(commit=False)
            accommodation_instance.user_info = user_instance
            accommodation_instance.save()
            # Redirect to a success page
        else:
            # Print errors to console (for debugging in development)
            print("User form errors:", user_form.errors)
            print("Accommodation form errors:", accommodation_form.errors)
    else:
        user_form = UserSignUpForm()
        accommodation_form = UserAccommodationInfoModel()

    return render(request, 'success.html', {
        'user_form': user_form,
        'accommodation_form': accommodation_form
    })

def success_view(request):
    return render(request, 'success.html')