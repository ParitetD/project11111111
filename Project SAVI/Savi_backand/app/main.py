from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
import shutil, os
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from app.database import engine, get_db, Base
from app import models
from app.schemas import PersonCreate, PersonOut

# Создаём таблицы при старте
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SAVI API", version="1.0")
from fastapi.staticfiles import StaticFiles
app.mount("/photos", StaticFiles(directory="."), name="photos")

# CORS — разрешаем фронтенду делать запросы
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # в продакшене укажи конкретный домен
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── GET /persons — список всех пропавших ───
@app.get("/persons", response_model=List[PersonOut])
def get_persons(
    status: str = None,   # ?status=Активен или ?status=Найден
    city: str = None,     # ?city=Москва
    db: Session = Depends(get_db)
):
    query = db.query(models.Person)

    if status:
        query = query.filter(models.Person.status == status)
    if city:
        query = query.filter(models.Person.city.ilike(f"%{city}%"))

    return query.order_by(models.Person.missing_date.desc()).all()


# ─── GET /persons/{id} — один человек ───
@app.get("/persons/{person_id}", response_model=PersonOut)
def get_person(person_id: int, db: Session = Depends(get_db)):
    person = db.query(models.Person).filter(models.Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Человек не найден")
    return person


# ─── POST /persons — добавить запись ───
@app.post("/upload")
async def upload_photo(file: UploadFile = File(...)):
    uploads_dir = "photos"
    os.makedirs(uploads_dir, exist_ok=True)
    file_path = f"{uploads_dir}/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"url": f"/photos/{file.filename}"}
@app.post("/persons", response_model=PersonOut, status_code=201)
def create_person(data: PersonCreate, db: Session = Depends(get_db)):
    person = models.Person(**data.model_dump())
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


# ─── PATCH /persons/{id}/found — отметить как найденного ───
@app.patch("/persons/{person_id}/found", response_model=PersonOut)
def mark_found(person_id: int, db: Session = Depends(get_db)):
    person = db.query(models.Person).filter(models.Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Человек не найден")
    person.status = models.StatusEnum.found
    db.commit()
    db.refresh(person)
    return person
