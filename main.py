from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Dictionary, SessionLocal
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware to accept requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Ibani Dictionary API!"}

@app.get("/search")
def search_word(word: str, db: Session = Depends(get_db)):
    try:
        if not word:
            raise HTTPException(status_code=400, detail="A search word must be provided")

          # Using regular expressions to match the exact word as a whole
        search_pattern = f"\\b{word.lower()}\\b"  # \\b is a word boundary anchor

        dictionary_entries = db.query(Dictionary).filter(func.lower(Dictionary.Meaning).op('REGEXP')(search_pattern)).all()
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
