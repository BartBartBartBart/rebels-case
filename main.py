from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, Base, get_db

# Create database if it doesn't exist
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()


@app.get("/")
def first_check():
    return {"status": "ok"}


# Insights endpoint (placeholder)
@app.get("/folder/insights")
def folder_insights(folder_path: str, db: Session = Depends(get_db)):
    return {"status": "insights ok", "folder": folder_path}


# Classification endpoint (placeholder)
@app.post("/folder/classify")
def folder_classify(folder_path: str, db: Session = Depends(get_db)):
    return {"status": "classify ok", "folder": folder_path}
