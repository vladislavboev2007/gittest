from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from models import Products
from database import get_db
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import datetime  # Добавьте эту строку

router = APIRouter(prefix="/products", tags=["products"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def read_products(request: Request, db: Session = Depends(get_db)):
    items = db.query(Products).all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "table": "products",
        "items": items,
        "columns": ["idproducts", "title", "descriptions"],
        "now_date": datetime.date.today().strftime("%Y-%m-%d")  # Добавили это
    })


@router.post("/")
async def create_product(
        request: Request,
        idproducts: int = Form(...),
        title: str = Form(...),
        descriptions: str = Form(default="Not description."),
        db: Session = Depends(get_db)
):
    db_product = Products(idproducts=idproducts, title=title, descriptions=descriptions)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    items = db.query(Products).all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "table": "products",
        "items": items,
        "columns": ["idproducts", "title", "descriptions"],
        "message": "Product added successfully!"
    })