import stripe

def valid_quantity_input(quantity:int):
    if quantity > 200:
        quantity = 200
    elif quantity < 10:
        quantity = 10
    else:
        quantity = 10
    return quantity

def find_customer(email:str, name:str):
    return stripe.Customer.search(
        query=f"email:\'{email}\' AND name:\'{name}\'",
        limit=1
    )

def create_customer(name: str, email: str, phone:str):
    stripe.Customer.create(
        email=email,
        name=name,
        phone=phone,
        payment_method="pm_card_visa",
        invoice_settings={"default_payment_method": "pm_card_visa"},
    )
