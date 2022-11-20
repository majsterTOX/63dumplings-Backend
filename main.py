from fastapi import FastAPI, APIRouter, Request, HTTPException, Form, Response
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fintech.checkout import create_checkout_session
from fintech.customer import find_customer, create_customer, valid_quantity_input

templates = Jinja2Templates(directory="templates")
router = APIRouter()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@router.get("/")
def order(request: Request):
    return templates.TemplateResponse('index.html', context={"request": request})


@router.post("/checkout")
def place_order(name: str = Form(...),
                email: str = Form(...),
                phone: str = Form(...),
                quantity: int = Form(...)):

    quantity = valid_quantity_input(quantity)

    try:
        cus_object = find_customer(email=email, name=name)
        cus_exist = bool(cus_object)

        if not cus_exist:
            create_customer(email=email, name=name, phone=phone)

        checkout = create_checkout_session(order_quantity=quantity)
    except Exception as e:
        return HTTPException(str(e))
    return RedirectResponse(checkout["url"], status_code=303)


@router.get('/success')
def success_payment_order(request: Request):
    return templates.TemplateResponse('success.html', context={"request": request})

@router.get('/cancel')
def cancel_payment_order(request: Request):
    return templates.TemplateResponse('cancel.html', context={"request": request})


app.include_router(router)
