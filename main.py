from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import os

from database import engine, Base, get_db
from services.insights import get_folder_insights, get_folder_classifications
from services.classifier import get_classifier

# Create database if it doesn't exist
Base.metadata.create_all(bind=engine)

# Instantiate model on startup
classifier = get_classifier(
    type=os.getenv("CLASSIFIER", "zero-shot")  # Default is zero-shot
)

# Initialize FastAPI app
app = FastAPI()


# API endpoint to show insights for given folder path
@app.post("/folder/insights")
def folder_insights(folder_path: str, db: Session = Depends(get_db)):
    insights = get_folder_insights(folder_path, db)
    return {"folder": folder_path, "insights": insights}


# API endpoint to classify documents in a given folder path
@app.post("/folder/classify")
def folder_classify(
    folder_path: str, overwrite: bool = False, db: Session = Depends(get_db)
):
    output = get_folder_classifications(classifier, folder_path, overwrite, db)
    return {
        "folder": folder_path,
        "num_files": output["num_files"],
        "new_classifications": output["new_classifications"],
        "already_classified": output["already_classified"],
    }
