from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from starlette.datastructures import URL
from starlette.templating import Jinja2Templates
from starlette import status
import validators
from pydantic import BaseModel, HttpUrl, validator
import datetime

from . import crud, models, schemas
from .config import get_settings
from .database import SessionLocal, engine

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://schort.it", "https://admin.schort.it", "https://api.schort.it"],
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="frontend/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_admin_info(db_url: models.URL) -> dict:
    base_url = URL(get_settings().base_url)
    short_endpoint = app.url_path_for("forward_to_target_url", url_key=db_url.key)
    admin_url = URL(get_settings().admin_url)

    return {
        "target_url": str(db_url.target_url),
        "is_active": db_url.is_active,
        "clicks": db_url.clicks,
        "date": db_url.date,
        "date_readable": datetime.datetime.fromtimestamp(float(db_url.date)).strftime("%d.%m.%Y %H:%M:%S"),
        "url": str(base_url.replace(path=short_endpoint)),
        "admin_url": f"{admin_url}/{db_url.secret_key}",
        "secret_key": db_url.secret_key,
    }

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

def raise_not_found(request):
    raise HTTPException(status_code=404, detail=f"URL '{request.url}' doesn't exist")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/linkus", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("linkus.html", {"request": request})

@app.post("/url")
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request("Your provided URL is not valid")

    db_url = crud.create_db_url(db=db, url=url)
    return {
        "url": f"https://api.schort.it/{db_url.key}",
        "admin_url": f"https://admin.schort.it/{db_url.secret_key}",
    }

@app.get("/{url_key}")
async def forward_to_target_url(url_key: str, request: Request, db: Session = Depends(get_db)):
    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        crud.update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_url)
    raise_not_found(request)

# Admin
@app.get("/admin/api/{secret_key}", response_model=schemas.URLInfo, name="admin_api")
async def admin_api(secret_key: str, request: Request, db: Session = Depends(get_db)):
    db_url = crud.get_db_url_by_secret_key(db, secret_key, include_inactive=True)
    if not db_url:
        raise_not_found(request)
    return get_admin_info(db_url)

@app.get("/admin-view/{secret_key}", response_class=HTMLResponse)
async def admin_view(request: Request, secret_key: str, db: Session = Depends(get_db)):
    db_url = crud.get_db_url_by_secret_key(db, secret_key, include_inactive=True)
    if not db_url:
        raise_not_found(request)
    data = get_admin_info(db_url)
    return templates.TemplateResponse("admin.html", {"request": request, "data": data, "secret_key": secret_key})

# Error
@app.post("/admin-view/{secret_key}/deactivate")
async def deactivate(secret_key: str, db: Session = Depends(get_db)):
    db_url = db.query(models.URL).filter(models.URL.secret_key == secret_key).first()
    if not db_url:
        raise_not_found(None)
    db_url.is_active = False
    db.commit()
    db.refresh(db_url)
    return {"detail": "deactivated"}

@app.post("/admin-view/{secret_key}/reactivate")
async def reactivate(secret_key: str, db: Session = Depends(get_db)):
    db_url = db.query(models.URL).filter(models.URL.secret_key == secret_key).first()
    if not db_url:
        raise_not_found(None)
    db_url.is_active = True
    db.commit()
    db.refresh(db_url)
    return {"detail": "reactivated"}

@app.delete("/admin-view/{secret_key}")
async def delete_url(secret_key: str, db: Session = Depends(get_db)):
    db_url = crud.get_db_url_by_secret_key(db, secret_key, include_inactive=True)
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    db.delete(db_url)
    db.commit()
    return {"detail": "deleted"}
