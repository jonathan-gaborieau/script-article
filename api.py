from bson import ObjectId
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
from pydantic import BaseModel
import motor.motor_asyncio
from methodScript import *
from celery_app import *

router = APIRouter()

# Paramètres MongoDB (vous pouvez les ajuster si nécessaire)
MONGO_URL = "mongodb+srv://contactformulaire96:5Dv0DajIWos5sjgD@cluster0.dkwv5dk.mongodb.net/"

# Client MongoDB
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.db_pages  # Remplacez par le nom de votre base de données

def document_to_dict(document: dict) -> dict:
    """
    Convertit un document MongoDB en dictionnaire compatible JSON.
    """
    # Convertit ObjectId en str
    if "_id" in document:
        document["_id"] = str(document["_id"])
    return document

class DataModel(BaseModel):
    option: str
    sujet: str = None
    type: str = None
    categorie: str = None
    ville: str = None

@router.post("/api/process_data")
async def process_data(data: DataModel):
    print("CREATION")
    process_data_celery.delay(data.option,data.sujet,data.ville,data.type,data.categorie)

# Dans api.py
@router.get("/sujets/")
async def get_all_sujets():
    sujets = []
    cursor = db.sujet.find({})
    async for document in cursor:
        sujets.append(document_to_dict(document))
    return sujets

@router.get("/villes/")
async def get_all_villes():
    villes = []
    cursor = db.ville.find({})
    async for document in cursor:
        villes.append(document_to_dict(document))
    return villes

class SujetUpdate(BaseModel):
    sujet: str
    type: str
    categorie: str

@router.put("/update_sujet/{sujet_id}")
async def update_sujet(sujet_id: str, updated_data: SujetUpdate):

    update_sujet_celery.delay(sujet_id,updated_data.sujet,updated_data.type,updated_data.categorie)

@router.put("/update_content/{sujet_id}")
async def update_sujet(sujet_id: str):
    update_sujet_celery_2.delay(sujet_id)

class VilleUpdate(BaseModel):
    ville: str

@router.put("/villes/{id}")
async def update_ville(id: str, ville_data: VilleUpdate):
    update_ville_celery.delay(id,ville_data.ville)

#API DU TEMPLATE SUJET

class Sujet(BaseModel):
    sujet: str

@router.post("/api/sujet_service")
async def ajouter_sujet(sujet: Sujet):
    ajouter_sujet_service.delay(sujet.sujet)

@router.delete("/api/sujet_service/{sujet_id}")
async def delete_sujet(sujet_id: str):
    delete_sujet_celery.delay(sujet_id)

@router.get("/api/sujet_service/{sujet_id}")
async def update_sujet_service_by_id(sujet_id: str):
    print("MISE A JOUR BEGIN")
    update_sujet_service_by_id_celery.delay(sujet_id)

class SujetUpdate(BaseModel):
    sujet: str

@router.put("/api/sujet_service/{sujet_id}")
async def update_sujet(sujet_id: str, updated_sujet: SujetUpdate):
    print("UPDATE SUJET")
    update_sujet_service_celery.delay(sujet_id,updated_sujet.sujet)

@router.get("/pages/")
async def get_all_pages():
    pages = []
    cursor = db.page.find({})
    async for document in cursor:
        pages.append(document_to_dict(document))
    return pages

@router.get("/download/")
async def download_project():
    folder_path = '../site-gestion-article'
    zip_path = 'dossier.zip'
    shutil.make_archive('dossier', 'zip', folder_path)
    return FileResponse(zip_path, media_type='application/octet-stream', filename='project.zip')
