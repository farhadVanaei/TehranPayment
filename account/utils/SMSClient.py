from abc import ABC, abstractmethod


class SMSClient(ABC):

    @abstractmethod
    def send_message(self, phone_number: str, message: str) -> dict:
        """Send an SMS message."""
        pass
