from celery import shared_task
from .models import SMSRequest, CustomUser
from django.core.exceptions import ObjectDoesNotExist
import logging
from .utils.sms_client_factory import SMSClientFactory

logger = logging.getLogger(__name__)

@shared_task
def send_sms_task(sms_request_id):
    try:
        sms_request = SMSRequest.objects.get(pk=sms_request_id)

        # Prepare the SMS content
        otp = sms_request.user.generate_otp()
        message = f"Your OTP code is: {otp}"
        phone_number = sms_request.user.phone_number

        # Send the SMS
        try:
            sms_client = SMSClientFactory().create_client()
            sms_client.send_message(phone_number, message)
            sms_request.status = 'sent'
        except:
            try:
                sms_request.threshold = sms_request.threshold + 1
            except:
                sms_request.status = 'failed'
        sms_request.save()
    except ObjectDoesNotExist:
        # Handle case where user or SMS request does not exist
        return False


@shared_task
def resend_pending_sms_requests():
    # Get all SMS requests with a status of 'pending'
    pending_requests = SMSRequest.objects.filter(status='pending')
    for request in pending_requests:
        logger.info(f"resend the sms request {request.user} - {request.id}")
        task = send_sms_task.delay(request.id)


