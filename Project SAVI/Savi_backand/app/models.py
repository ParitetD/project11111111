from sqlalchemy import Column, Integer, String, Date, Enum, Text
from app.database import Base
import enum


class StatusEnum(str, enum.Enum):
    active = "Активен"
    found = "Найден"


class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)       # ФИО
    age = Column(Integer, nullable=False)                  # Возраст
    city = Column(String(100), nullable=False)             # Город
    missing_date = Column(Date, nullable=False)            # Дата пропажи
    clothes = Column(Text, nullable=False)                 # Описание одежды
    features = Column(Text, nullable=False)                # Особые приметы
    photo_url = Column(String(500), nullable=True)         # Ссылка на фото
    status = Column(Enum(StatusEnum), default=StatusEnum.active)  # Статус
    contact_phone = Column(String(20), nullable=False)     # Телефон для связи
