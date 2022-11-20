import stripe
import os
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

DOMAIN_URL = os.getenv("DOMAIN_URL")
DUMPLINGS_PRICE_ID = os.getenv("DUMPLINGS_PRICE_ID")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
stripe.api_version = os.getenv("STRIPE_API_VERSION")


def create_checkout_session(order_quantity: int):
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': DUMPLINGS_PRICE_ID,
                    'quantity': order_quantity
                }
            ],
            mode='payment',
            success_url=DOMAIN_URL + '/success',
            cancel_url=DOMAIN_URL + '/cancel',
            payment_method_types=['card']
        )
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))
    return checkout_session