from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

app = FastAPI(
    title="MAREC HR360 API",
    description="HR Intelligence Platform Backend",
    version="1.0"
)

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.get("/")
def root():
    return {"message": "MAREC HR360 API running"}


@app.get("/ping")
def ping():
    return {"status": "API alive"}


@app.post("/register")
def register(data: dict):
    company = data.get("company")
    email = data.get("email")

    return {
        "status": "workspace created",
        "company": company,
        "admin": email
    }


@app.post("/login")
def login(data: dict):
    email = data.get("email")

    return {
        "token": "demo-token",
        "company": "Demo Workspace",
        "email": email
    }


@app.post("/upload")
async def upload(files: list[UploadFile] = File(...)):

    saved_files = []

    for file in files:

        path = f"{UPLOAD_FOLDER}/{file.filename}"

        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        saved_files.append(file.filename)

    return {
        "status": "files uploaded",
        "files": saved_files
    }
