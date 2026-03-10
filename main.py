from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from services.insights import get_folder_insights

# Create database if it doesn't exist
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()


# API endpoint to show insights for given folder path
@app.get("/folder/insights")
def folder_insights(folder_path: str, db: Session = Depends(get_db)):
    insights = get_folder_insights(folder_path, db)
    return {"folder": folder_path, "insights": insights}


# Classification endpoint (placeholder)
@app.post("/folder/classify")
def folder_classify(folder_path: str, db: Session = Depends(get_db)):
    return {"status": "classify ok", "folder": folder_path}
