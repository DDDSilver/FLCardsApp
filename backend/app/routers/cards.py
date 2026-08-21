from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(tags=["cards"])

@router.post("/decks/{deck_id}/cards", response_model=schemas.Card)
def create_card(deck_id: int, card: schemas.CardCreate, db: Session = Depends(get_db)):
    deck = db.query(models.Deck).filter(models.Deck.id == deck.id).first()
    if deck is None:
        raise HTTPException(status_code=404, detail="Deck does not exist")\

    new_card = models.Card(deck_id=deck_id, front=card.front, back=card.back)
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return new_card

@router.get("/cards/{card_id}", response_model=schemas.Card)
def get_card(card_id: int, db: Session = Depends(get_db)):
    card = db.query(models.Card).filter(models.Card.id == card_id).first()
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return card
 
 
@router.put("/cards/{card_id}", response_model=schemas.Card)
def update_card(card_id: int, updated: schemas.CardCreate, db: Session = Depends(get_db)):
    card = db.query(models.Card).filter(models.Card.id == card_id).first()
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    card.front = updated.front
    card.back = updated.back
    db.commit()
    db.refresh(card)
    return card
 
 
@router.delete("/cards/{card_id}")
def delete_card(card_id: int, db: Session = Depends(get_db)):
    card = db.query(models.Card).filter(models.Card.id == card_id).first()
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    db.delete(card)
    db.commit()
    return {"detail": "Card deleted"}