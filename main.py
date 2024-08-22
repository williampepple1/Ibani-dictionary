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
def search_word(word: str, db: Session = Depends(get_db)):
    try:
        if not word:
            raise HTTPException(status_code=400, detail="A search word must be provided")

        # Query the `Meaning` column for entries containing the search term
        dictionary_entries = db.query(Dictionary).filter(Dictionary.Meaning.ilike(f"%{word}%")).all()

        if not dictionary_entries:
            raise HTTPException(status_code=404, detail="No words associated with this meaning are found in the dictionary")

        return [
            {
                "Ibani": entry.Ibani,
                "Pos": entry.Pos,
                "Meaning": entry.Meaning
            } for entry in dictionary_entries
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
