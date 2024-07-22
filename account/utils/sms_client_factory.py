from django.conf import settings
import time

from .SMSClient import SMSClient
from .SMSClientServiceOne import SMSClientServiceOne
from .SMSClientServiceTwo import SMSClientServiceTwo


class SMSClientFactory:
    @staticmethod
    def create_client() -> SMSClient:
        provider = settings.SMS_PROVIDER
        retry_attempts = settings.SMS_RETRY_ATTEMPTS
        retry_delay = settings.SMS_RETRY_DELAY

        for attempt in range(retry_attempts):
            try:
                if provider == 'service_one':
                    return SMSClientServiceOne(
                        api_key=settings.SERVICE_ONE_API_KEY,
                        api_secret=settings.SERVICE_ONE_API_SECRET
                    )
                elif provider == 'service_two':
                    return SMSClientServiceTwo(
                        token=settings.SERVICE_TWO_TOKEN,
                        sender_id=settings.SERVICE_TWO_SENDER_ID
                    )
                else:
                    raise ValueError(f"Unsupported SMS provider: {provider}")
            except Exception as e:
                if attempt < retry_attempts - 1:
                    time.sleep(retry_delay)  # Wait before retrying
                else:
                    raise e  # Reraise the exception if all attempts fail
