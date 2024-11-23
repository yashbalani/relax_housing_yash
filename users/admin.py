from django.contrib import admin
from .models import MinLengthOfStayModel, PurposeOfStayModel, UserLocationDetailsModel, UserModel, RoomPreferenceModel, LifestylePreferenceModel, InterestModel, UserAccommodationInfoModel,AdditionalPreferenceModel
from location.models import CitiesModel  # Assuming location is an external app for cities

# Registering the RoomPreferenceModel
@admin.register(RoomPreferenceModel)
class RoomPreferenceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(AdditionalPreferenceModel)
class AdditionalPreferenceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

# Registering the LifestylePreferenceModel
@admin.register(LifestylePreferenceModel)
class LifestylePreferenceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

# Registering the InterestModel
@admin.register(InterestModel)
class InterestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

# Registering the UserModel
@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'is_verified']
    search_fields = ['first_name', 'last_name', 'date_of_birth', 'gender']
    list_filter = ['gender', 'is_verified']
    ordering = ['-created_at']

# Registering the AccommodationInfoModel
@admin.register(UserAccommodationInfoModel)
class UserAccommodationInfoAdmin(admin.ModelAdmin):
    list_display = ['user_info', 'city_origin', 'city_accommodation', 'purpose_of_stay', 'room_preference', 'min_budget', 'max_budget', 'lifestyle']
    search_fields = ['purpose_of_stay', 'room_preference__name', 'lifestyle__name']
    list_filter = ['purpose_of_stay', 'room_preference', 'lifestyle']
    ordering = ['user_info__first_name']

# Registering the CitiesModel
@admin.register(CitiesModel)
class CitiesModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(PurposeOfStayModel)
class PurposeOfStayModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(MinLengthOfStayModel)
class MinLengthOfStayModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(UserLocationDetailsModel)
class UserLocationDetailsModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'country_id']
    search_fields = ['country_id']