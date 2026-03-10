from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def first_check():
    return {"status": "ok"}


@app.get("/folder/insights")
def folder_insights(folder_path: str):
    return {"status": "insights ok", "folder": folder_path}


@app.post("/folder/classify")
def folder_classify(folder_path: str):
    return {"status": "classify ok", "folder": folder_path}
