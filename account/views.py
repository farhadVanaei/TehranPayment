from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from account.tasks import send_sms_task
from account.models import SMSRequest, CustomUser as User
from account.serializers import RegisterSerializer, OTPRequestSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class MyTokenObtainPairView(TokenObtainPairView):
    pass


class MyTokenRefreshView(TokenRefreshView):
    pass


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": RegisterSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        }, status=status.HTTP_201_CREATED)


class GenerateOTPView(generics.GenericAPIView):
    serializer_class = OTPRequestSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(pk=request.user.id).first()
        sms_request = SMSRequest.objects.create(
            user=user,
            task_id='',
            status='pending'
        )
        sms_request.save()
        task = send_sms_task.delay(sms_request.id)
        sms_request.task_id = task.id
        sms_request.save()

        return Response({
            "message": "OTP has been sent to your phone number."
        }, status=status.HTTP_200_OK)