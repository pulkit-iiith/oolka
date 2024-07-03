from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def create_checkout_session(self, amount: int, currency: str, description: str, success_url: str, cancel_url: str):
        pass
