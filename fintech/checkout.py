import stripe
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from product import Product

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
stripe.api_version = os.getenv("STRIPE_API_VERSION")

DOMAIN = "http://127.0.0.1:8000"


def create_checkout_session(order_quantity: int):
    try:
        dumplings = Product(
            name="Pierogi Ruskie", price_id="price_1LNTGJFapr9QmkPSJ8S8HI3W", quantity=order_quantity)

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': dumplings.price_id,
                    'quantity': dumplings.quantity
                }
            ],
            mode='payment',
            success_url=DOMAIN + '/success',
            cancel_url=DOMAIN + '/cancel',
            payment_method_types=['card']
        )
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))
    return checkout_session
