from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Dictionary, SessionLocal

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/search")
def search_word(ibani: str, db: Session = Depends(get_db)):
    if not ibani:
        raise HTTPException(status_code=400, detail="A search word must be provided")

    dictionary_entry = db.query(Dictionary).filter(Dictionary.ibani == ibani.lower()).first()

    if not dictionary_entry:
        raise HTTPException(status_code=404, detail="Word not found")

    return {
        "ibani": dictionary_entry.ibani,
        "pos": dictionary_entry.pos,
        "meaning": dictionary_entry.meaning
    }
