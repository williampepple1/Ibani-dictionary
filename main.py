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
    try:
        if not ibani:
            raise HTTPException(status_code=400, detail="A search word must be provided")

        # Use the correct column name casing
        dictionary_entry = db.query(Dictionary).filter(Dictionary.Ibani == ibani).first()

        if not dictionary_entry:
            raise HTTPException(status_code=404, detail="Word not found")

        return {
            "Ibani": dictionary_entry.Ibani,
            "Pos": dictionary_entry.Pos,
            "Meaning": dictionary_entry.Meaning
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
