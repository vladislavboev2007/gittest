from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from routers import percent, products, profit, register
from datetime import datetime
import datetime



models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SalesDB Management System")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(percent.router)  # Изменили
app.include_router(products.router)
app.include_router(profit.router)
app.include_router(register.router)

templates = Jinja2Templates(directory="templates")


@app.get("/home", response_class=HTMLResponse)
async def home_page(request: Request, db: Session = Depends(get_db)):
    """Альтернативный маршрут для домашней страницы"""
    from models import Percent, Products, Profit, Register
    counts = {
        "percent": db.query(Percent).count(),
        "products": db.query(Products).count(),
        "profit": db.query(Profit).count(),
        "register": db.query(Register).count()
    }

    return templates.TemplateResponse("index.html", {
        "request": request,
        "table": "home",
        "counts": counts
    })


@app.get("/switch/{table}")
async def switch_table(table: str):
    return RedirectResponse(f"/{table}/")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)