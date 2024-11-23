import django
from django.db import models

from location.models import CitiesModel

# Room preference model (For shared/private room options)
class RoomPreferenceModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class AdditionalPreferenceModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Lifestyle preference model (For introverted/extroverted/quiet etc.)
class LifestylePreferenceModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Hobbies and Interests model
class InterestModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MinLengthOfStayModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class PurposeOfStayModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
# User model
class UserModel(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.CharField(max_length=100,default="")
    password = models.CharField(default="",blank=False)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15, blank=False, null=True,error_messages={"unique": "This phone number already exists in our database"},)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=False, null=True)
    gender = models.CharField(max_length=10)
    passport = models.FileField(
        upload_to='passports/', 
        null=False, 
        blank=False, 
        help_text="Passport file as identity proof",
        default='/Users/apple/Downloads/relax_housing/passport_default_file.jpeg'
    )    # Additional fields
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    interests = models.ManyToManyField(InterestModel, related_name="users")
    # Auto timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class UserLocationDetailsModel(models.Model):
    """Model for storing user city,state and country"""

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True)
    state_id = models.IntegerField(blank=True, default=0)
    city_id = models.IntegerField(blank=True, default=0)
    city_name = models.CharField(max_length=200, default="")
    country_id = models.IntegerField(blank=True, default=0)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=False)
    objects = models.Manager()
    
class UserAccommodationInfoModel(models.Model):
    # ForeignKey to PersonalInfoModel for linking the user's information
    user_info = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    start_date = models.DateField(default=None)
    min_length_of_stay = models.ForeignKey(MinLengthOfStayModel, related_name="min_stay", on_delete=models.CASCADE,default=None)
    # Location of Origin and Accommodation
    city_origin = models.ForeignKey(CitiesModel, related_name="origin_city", on_delete=models.CASCADE)
    city_accommodation = models.ForeignKey(CitiesModel, related_name="accommodation_city", on_delete=models.CASCADE)
    
    # Purpose of stay and accommodation details
    purpose_of_stay = models.ForeignKey(PurposeOfStayModel, related_name="purpose_of_stay", on_delete=models.CASCADE)
    room_preference = models.ForeignKey(RoomPreferenceModel, on_delete=models.CASCADE)
    additional_preference = models.ForeignKey(AdditionalPreferenceModel, on_delete=models.CASCADE,null=True)
    min_budget = models.DecimalField(max_digits=10, decimal_places=2)
    max_budget = models.DecimalField(max_digits=10, decimal_places=2)
    lifestyle = models.ForeignKey(LifestylePreferenceModel, on_delete=models.CASCADE)
    