from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
 
from .. import models, schemas
from ..database import get_db
 
router = APIRouter(prefix="/decks", tags=["decks"])
 
 
@router.post("/", response_model=schemas.Deck)
def create_deck(deck: schemas.DeckCreate, db: Session = Depends(get_db)):
    new_deck = models.Deck(name=deck.name, description=deck.description)
    db.add(new_deck)
    db.commit()
    db.refresh(new_deck)
    return new_deck
 
 
@router.get("/", response_model=list[schemas.Deck])
def list_decks(db: Session = Depends(get_db)):
    return db.query(models.Deck).all()
 
 
@router.get("/{deck_id}", response_model=schemas.Deck)
def get_deck(deck_id: int, db: Session = Depends(get_db)):
    deck = db.query(models.Deck).filter(models.Deck.id == deck_id).first()
    if deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    return deck
 
 
@router.put("/{deck_id}", response_model=schemas.Deck)
def update_deck(deck_id: int, updated: schemas.DeckCreate, db: Session = Depends(get_db)):
    deck = db.query(models.Deck).filter(models.Deck.id == deck_id).first()
    if deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    deck.name = updated.name
    deck.description = updated.description
    db.commit()
    db.refresh(deck)
    return deck
 
 
@router.delete("/{deck_id}")
def delete_deck(deck_id: int, db: Session = Depends(get_db)):
    deck = db.query(models.Deck).filter(models.Deck.id == deck_id).first()
    if deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    db.delete(deck)
    db.commit()
    return {"detail": "Deck deleted"}