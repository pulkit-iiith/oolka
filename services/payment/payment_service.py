from .payment_processor import PaymentProcessor

class PaymentService:
    def __init__(self, processor: PaymentProcessor):
        self.processor = processor

    def create_checkout_session(self, amount: int, currency: str, description: str, success_url: str, cancel_url: str):
        return self.processor.create_checkout_session(amount, currency, description, success_url, cancel_url)

