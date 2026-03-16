from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
import os
import urllib.parse

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


def check_path(folder: str) -> str:
    # Decode URL-encoded paths (e.g. spaces encoded as %20 or +) and strip quotes.
    folder = urllib.parse.unquote_plus(str(folder)).strip('"')

    path = Path(folder).expanduser().resolve()

    if not path.exists():
        raise HTTPException(status_code=400, detail="Folder does not exist.")

    if not path.is_dir():
        raise HTTPException(status_code=400, detail="Provided path is not a directory.")

    return str(path)


# API endpoint to show insights for given folder path
@app.post("/folder/insights")
def folder_insights(folder_path: str, db: Session = Depends(get_db)):
    folder_path = check_path(folder_path)
    output = get_folder_insights(folder_path, db)
    return {
        "folder": str(folder_path),
        "num_files": output["num_files"],
        "insights": output["insights"],
    }


# API endpoint to classify documents in a given folder path
@app.post("/folder/classify")
def folder_classify(
    folder_path: str, overwrite: bool = False, db: Session = Depends(get_db)
):
    folder_path = check_path(folder_path)
    output = get_folder_classifications(classifier, folder_path, overwrite, db)
    return {
        "folder": str(folder_path),
        "num_files": output["num_files"],
        "classifications": output["classifications"],
    }
