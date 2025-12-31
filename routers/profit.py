from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from models import Profit
from database import get_db
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import datetime

router = APIRouter(prefix="/profit", tags=["profit"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def read_profit(request: Request, db: Session = Depends(get_db)):
    items = db.query(Profit).all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "table": "profit",
        "items": items,
        "columns": ["idprofit", "ts", "idregister", "quantice", "price", "total", "n_profit", "rate"],
        "now_date": datetime.date.today().strftime("%Y-%m-%d")  # Добавили это
    })


@router.post("/")
async def create_profit(
        request: Request,
        idregister: int = Form(...),
        quantice: int = Form(...),
        price: float = Form(...),
        total: float = Form(...),
        db: Session = Depends(get_db)
):
    # Note: n_profit and rate will be calculated by trigger
    db_profit = Profit(
        idregister=idregister,
        quantice=quantice,
        price=price,
        total=total,
        ts=datetime.datetime.now(),
        n_profit=0,  # Will be set by trigger
        rate=0  # Will be set by trigger
    )
    db.add(db_profit)
    db.commit()
    db.refresh(db_profit)

    items = db.query(Profit).all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "table": "profit",
        "items": items,
        "columns": ["idprofit", "ts", "idregister", "quantice", "price", "total", "n_profit", "rate"],
        "message": "Profit record added successfully!"
    })