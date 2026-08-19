from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class CardBase(BaseModel):
    front: str
    back: str

class CardCreate(CardBase):
    pass

class Card(CardBase):
    id: int
    deck_id: int
    ease_factor: float
    interval_days: int
    repetitions: int
    next_review_date: date

    class Config:
        from_attributes = True


class DeckBase(BaseModel):
    name: str
    description: Optional[str] = None

class DeckCreate(DeckBase):
    pass

class Deck(DeckBase):
    id: int
    created_at: datetime
    cards: list[Card] = []

    class Config:
        from_attributes = True