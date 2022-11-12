from fastapi import FastAPI, APIRouter, Request, HTTPException, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fintech.checkout import create_checkout_session

templates = Jinja2Templates(directory="templates")
router = APIRouter()


def setup():
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(router)
    return app


@router.get("/")
def order(request: Request):
    return templates.TemplateResponse('order.html', context={"request": request})

@router.post("/create-checkout-session")
def place_order(request: Request,
                name: str = Form(...),
                email: str = Form(...),
                quantity: int = Form(...)):
    try:
        checkout = create_checkout_session(order_quantity=quantity)
    except Exception as e:
        raise HTTPException(str(e))
    return RedirectResponse(checkout["url"], status_code=303)

@router.get('/success')
def success_payment_order(request: Request):
    return templates.TemplateResponse('success.html', context={"request": request})


@router.get('/cancel')
def cancel_payment_order(request: Request):
    return templates.TemplateResponse('cancel.html', context={"request": request})


app = setup()
