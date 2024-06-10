from .payment_processor import PaymentProcessor

class PaymentService:
    def __init__(self, processor: PaymentProcessor):
        self.processor = processor

    def process_payment(self, amount: int, currency: str, source: str, description: str):
        return self.processor.process_payment(amount, currency, source, description)
