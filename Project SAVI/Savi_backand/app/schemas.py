from pydantic import BaseModel, field_validator
from datetime import date
from typing import Optional
from app.models import StatusEnum


# Список запрещённых слов (мат и спам)
BANNED_WORDS = [
    # мат
    "блядь", "бляд", "хуй", "хуя", "пизда", "пизд", "ебать", "еб",
    "пиздец", "залупа", "мудак", "ёбаный", "ёб", "сука", "cука",
    # спам
    "казино", "заработок", "кредит", "займ", "нажми", "перейди",
    "бесплатно", "выиграй", "http://", "https://t.me", "telegram",
    "подпишись", "реклама",
]


def check_banned(text: str) -> str:
    text_lower = text.lower()
    for word in BANNED_WORDS:
        if word in text_lower:
            raise ValueError(f"Текст содержит запрещённое слово или спам")
    return text


# Схема для создания записи (POST)
class PersonCreate(BaseModel):
    full_name: str
    age: int
    city: str
    missing_date: date
    clothes: str
    features: str
    photo_url: Optional[str] = None
    contact_phone: str

    @field_validator("clothes", "features", "full_name")
    @classmethod
    def validate_no_banned(cls, v):
        return check_banned(v)

    @field_validator("age")
    @classmethod
    def validate_age(cls, v):
        if v < 0 or v > 120:
            raise ValueError("Возраст должен быть от 0 до 120")
        return v


# Схема для ответа (GET) — то что видит фронтенд
class PersonOut(BaseModel):
    id: int
    full_name: str
    age: int
    city: str
    missing_date: date
    clothes: str
    features: str
    photo_url: Optional[str]
    status: StatusEnum
    contact_phone: str

    class Config:
        from_attributes = True
