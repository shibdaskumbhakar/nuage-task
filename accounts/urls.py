from django.contrib import admin
from django.urls import path
from .views import CustomTokenObtainPairView, RegisterUserView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'accounts' 

urlpatterns = [
    path('token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup', RegisterUserView.as_view(), name='signup'),
]