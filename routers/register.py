from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from models import Register, Products
from database import get_db
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import datetime

router = APIRouter(prefix="/register", tags=["register"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def read_register(request: Request, db: Session = Depends(get_db)):
    items = db.query(Register).join(Products, Register.product == Products.idproducts).all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "table": "register",
        "items": items,
        "columns": ["idregister", "ts", "product", "quantite", "price", "total", "n_total", "n_quantite", "n_price"],
        "show_products": True,
        "now_date": datetime.date.today().strftime("%Y-%m-%d")  # Добавили это
    })


@router.post("/")
async def create_register(
        request: Request,
        product: int = Form(...),
        quantite: int = Form(...),
        price: float = Form(...),
        db: Session = Depends(get_db)
):
    # Note: total, n_total, n_quantite, n_price will be calculated by trigger
    db_register = Register(
        product=product,
        quantite=quantite,
        price=price,
        ts=datetime.datetime.now(),
        total=0,  # Will be calculated by trigger
        n_total=None,
        n_quantite=None,
        n_price=None
    )
    db.add(db_register)
    db.commit()
    db.refresh(db_register)

    items = db.query(Register).join(Products, Register.product == Products.idproducts).all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "table": "register",
        "items": items,
        "columns": ["idregister", "ts", "product", "quantite", "price", "total", "n_total", "n_quantite", "n_price"],
        "show_products": True,
        "message": "Register record added successfully!"
    })