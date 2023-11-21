from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import motor.motor_asyncio
from bson import ObjectId
from fastapi.responses import FileResponse
from pydantic import BaseModel
from api import router as api_router
from wordpressModule1 import delete_page
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from celery_app import delete_item_celery


templates = Jinja2Templates(directory="templates")

def document_to_dict(document: dict) -> dict:
    """
    Convertit un document MongoDB en dictionnaire compatible JSON.
    """
    # Convertit ObjectId en str
    if "_id" in document:
        document["_id"] = str(document["_id"])
    return document


app = FastAPI()
app.include_router(api_router)
security = HTTPBasic()

# Paramètres MongoDB
MONGO_URL = "mongodb+srv://contactformulaire96:5Dv0DajIWos5sjgD@cluster0.dkwv5dk.mongodb.net/?ssl=true&ssl_cert_reqs=CERT_NONE"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.db_pages  # Remplacez par le nom de votre base de données

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = client
    app.mongodb = db

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "lgi")
    correct_password = secrets.compare_digest(credentials.password, "lgipass123")
    
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/private/")
async def read_private_zone(username: str = Depends(get_current_username)):
    # Ici, vous pouvez interagir avec votre base de données si nécessaire
    document = await db.page.find_one() 
    return {"message": f"Hello, {username}", "data": document}

@app.get("/")
async def read_root(credentials: HTTPBasicCredentials = Depends(security)):
    return FileResponse("template.html")

@app.get("/ajout-sujet")
async def read_sujet(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    cursor = db.sujet_service.find()
    sujets = await cursor.to_list(length=100)
    sujets = [document_to_dict(doc) for doc in sujets]
    return templates.TemplateResponse("template_sujet.html", {"request": request, "sujets": sujets})


@app.delete("/api/delete/{collection_type}/{item_id}")
async def delete_item(collection_type: str, item_id: str):
    print("ICILA")
    delete_item_celery.delay(collection_type, item_id)
    return {"message": "Notification sent in the background"}

