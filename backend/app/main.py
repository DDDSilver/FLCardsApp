from fastapi import FastAPI
from . import models
from .database import engine
from .routers import decks, cards

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FLCardsApp API")

app.include_router(decks.router)
app.include_router(cards.router)

@app.get("/")
def root():
    return {"status": "running"}
