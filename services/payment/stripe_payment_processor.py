import stripe
from .payment_processor import PaymentProcessor


class StripeAdapter(PaymentProcessor):
    def __init__(self, api_key: str):
        stripe.api_key = api_key

    def create_checkout_session(
        self,
        amount: int,
        currency: str,
        description: str,
        success_url: str,
        cancel_url: str,
        metadata: dict = None,
    ):
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": currency,
                            "product_data": {
                                "name": description,
                            },
                            "unit_amount": amount,
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=success_url,
                cancel_url=cancel_url,
                metadata=metadata,
            )
            return session
        except stripe.error.StripeError as e:
            raise ValueError(f"Checkout session creation failed: {e.user_message}")
