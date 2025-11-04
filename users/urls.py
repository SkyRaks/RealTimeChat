from django.urls import path
from users.views import *

urlpatterns = [
    path('', profile_view, name="profile"),
    path('edit/', profile_edit_view, name="profile_edit"),
    path('onboarding/', profile_edit_view, name="profile-onboarding"),
    path('settings/', profile_settings_view, name="profile-settings"),
    path('emailchange/', profile_email_change, name="profile-emailchange"),
]
