from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from models import Percent  # Изменили импорт
from database import get_db
from typing import List
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import datetime

router = APIRouter(prefix="/percent", tags=["percent"])  # Изменили префикс
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def read_percent(request: Request, db: Session = Depends(get_db)):
    items = db.query(Percent).all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "table": "percent",
        "items": items,
        "columns": ["idpecent", "ts", "rate"],
        "now_date": datetime.date.today().strftime("%Y-%m-%d")  # Добавили это
    })


@router.post("/")
async def create_percent(  # Изменили имя функции
        request: Request,
        rate: float = Form(...),
        ts: str = Form(default=None),
        db: Session = Depends(get_db)
):
    if not ts:
        ts = datetime.date.today()
    else:
        ts = datetime.datetime.strptime(ts, "%Y-%m-%d").date()

    db_percent = Percent(ts=ts, rate=rate)  # Используем модель Percent
    db.add(db_percent)
    db.commit()
    db.refresh(db_percent)

    items = db.query(Percent).all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "table": "percent",  # Изменили на percent
        "items": items,
        "columns": ["idpercent", "ts", "rate"],
        "message": "Record added successfully!"
    })


@router.delete("/{id}")
async def delete_percent(id: int, db: Session = Depends(get_db)):  # Изменили имя функции
    item = db.query(Percent).filter(Percent.idpercent == id).first()  # Используем модель Percent
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item deleted"}