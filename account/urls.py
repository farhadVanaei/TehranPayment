from django.urls import path
from .views import RegisterView, MyTokenObtainPairView, MyTokenRefreshView, GenerateOTPView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('generate-otp/', GenerateOTPView.as_view(), name='generate-otp'),
]

