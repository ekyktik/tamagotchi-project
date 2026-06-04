from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TamagotchiState(BaseModel):
    "Стан тамагочі"
    name: str = "Піксель"
    hunger: int = Field(default=50, ge=0, le=100, description="Рівень голоду (0=ситий, 100=голодний)")
    happiness: int = Field(default=50, ge=0, le=100, description="Рівень щастя (0=сумний, 100=щасливий)")
    energy: int = Field(default=50, ge=0, le=100, description="Рівень енергії (0=втомлений, 100=бадьорий)")
    age: int = Field(default=0, description="Вік у хвилинах")
    is_alive: bool = True
    last_updated: str = Field(default_factory=lambda: datetime.now().isoformat())


class FeedRequest(BaseModel):
    "Запит на годування"
    food_type: str = Field(default="basic", description="Тип їжі: basic, treat, healthy")


class PlayRequest(BaseModel):
    """Запит на гру"""
    activity: str = Field(default="ball", description="Вид активності: ball, puzzle, dance")


class StatusResponse(BaseModel):
    """Відповідь зі станом тамагочі"""
    name: str
    hunger: int
    happiness: int
    energy: int
    age: int
    is_alive: bool
    mood: str
    emoji: str
    last_updated: str


class ActionResponse(BaseModel):
    """Відповідь після дії"""
    success: bool
    message: str
    state: StatusResponse


class ErrorResponse(BaseModel):
    """Відповідь з помилкою"""
    detail: str
    code: str