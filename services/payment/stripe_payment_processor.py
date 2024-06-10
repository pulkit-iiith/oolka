import stripe
from .payment_processor import PaymentProcessor

class StripeAdapter(PaymentProcessor):
    def __init__(self, api_key: str):
        stripe.api_key = api_key

    def process_payment(self, amount: int, currency: str, source: str, description: str):
        try:
            # charge = stripe.Charge.create(
            #     amount=amount,
            #     currency=currency,
            #     source=source,
            #     description=description
            # )
            # return charge
            print({"amount":amount,
                "currency":currency,
                "source":source,
                "description":description})
        except stripe.error.StripeError as e:
            raise ValueError(f"Payment failed: {e.user_message}")
