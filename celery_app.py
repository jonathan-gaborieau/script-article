# celery_app.py
import asyncio
from celery import Celery
from methodScript import *
from pydantic import BaseModel
import motor.motor_asyncio
from bson import ObjectId
from fastapi import HTTPException

# Paramètres MongoDB (vous pouvez les ajuster si nécessaire)
MONGO_URL = "mongodb+srv://contactformulaire96:5Dv0DajIWos5sjgD@cluster0.dkwv5dk.mongodb.net/"

# Client MongoDB
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.db_pages  # Remplacez par le nom de votre base de données

celery_app = Celery("fastapi_celery")
celery_app.config_from_object('celery_config')
global_loop = asyncio.new_event_loop()

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

@celery_app.task
def process_data_celery(option,sujet,ville,type,categorie):
    asyncio.set_event_loop(global_loop)
    
    # Exécuter le code asynchrone dans cette boucle
    result = global_loop.run_until_complete(_async_process_data_celery( option, sujet, ville, type, categorie))
    
    return result
async def _async_process_data_celery(option,sujet,ville,type,categorie):
    if option == "sujet":
        # Créez un dictionnaire pour les données du sujet
        sujet_data = {
            "sujet": sujet,
            "type": type,
            "categorie": categorie
        }
        print("LESCATEGORIES")

        # Insérer les données dans la collection "sujet"
        db.sujet.insert_one(sujet_data)
        print("DEBUT GENERATE")
        result = await generate_content_for_all_cities(sujet, type, categorie)

        if result:
            return {"message": "Données sujet enregistrées avec succès"}
        else:
            raise HTTPException(status_code=500, detail="Erreur lors de l'enregistrement des données sujet")

    elif option == "ville":
        # Créez un dictionnaire pour les données de la ville
        ville_data = {"ville": ville}

        # Insérer les données dans la collection "ville" (ou tout autre nom que vous préférez pour la collection des villes)
        db.ville.insert_one(ville_data)

        print("DEBUT GENERATE VILLE")
        result = await generate_content_for_all_subject(ville)

        if result:
            return {"message": "Données ville enregistrées avec succès"}
        else:
            raise HTTPException(status_code=500, detail="Erreur lors de l'enregistrement des données ville")

    else:
        raise HTTPException(status_code=400, detail="Option invalide")

class SujetUpdate(BaseModel):
    sujet: str
    type: str
    categorie: str

@celery_app.task
def update_sujet_celery(sujet_id: str, sujet, type, categorie):
    asyncio.set_event_loop(global_loop)
    
    # Exécuter le code asynchrone dans cette boucle
    result = global_loop.run_until_complete(_async_update_sujet_celery(sujet_id, sujet, type, categorie))
    
    return result

async def _async_update_sujet_celery(sujet_id: str, sujet_new, type, categorie):
    # Convertir sujet_id en ObjectId
    try:
        obj_id = ObjectId(sujet_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid sujet_id format")
    sujet = await db.sujet.find_one({"_id": ObjectId(obj_id)})
        
        # Si le sujet est trouvée
    if sujet:
        # Affiche le sujet actuelle
        print("LE SUJET AVANT LA MODIFICATION:")
        print(sujet['sujet'])
        pages_cursor = db.page.find({"sujet": sujet['sujet']})

        for page in await pages_cursor.to_list(length=9999):
            print(page['_id'])
            mise_a_jour_contenu(str(page['id_page']),sujet_new, page['ville'], type)
            db.page.update_one({"_id": ObjectId(page['_id'])}, {"$set": {"sujet": sujet_new}})
        # Mettre à jour le document
        result = await db["sujet"].update_one(
            {"_id": obj_id},
            {"$set": {
                "sujet": sujet_new,
                "type": type,
                "categorie": categorie
            }}
        )
    
    # Vérifier si le document a été mis à jour
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Sujet not found")
    
    return {"status": "success", "message": "Sujet modifier avec succès"}

@celery_app.task
def update_sujet_celery_2(sujet_id: str):
    asyncio.set_event_loop(global_loop)
    
    # Exécuter le code asynchrone dans cette boucle
    result = global_loop.run_until_complete(_async_update_sujet_celery_2(sujet_id))
    
    return result
async def _async_update_sujet_celery_2(sujet_id: str):
    # Convertir sujet_id en ObjectId
    try:
        obj_id = ObjectId(sujet_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid sujet_id format")
    sujet = await db.sujet.find_one({"_id": ObjectId(obj_id)})
        
        # Si le sujet est trouvée
    if sujet:
        # Affiche le sujet actuelle
        print("LE SUJET AVANT LA MODIFICATION:")
        print(sujet['sujet'])
        pages_cursor = db.page.find({"sujet": sujet['sujet']})

        for page in await pages_cursor.to_list(length=9999):
            print(page['_id'])
            mise_a_jour_contenu(str(page['id_page']),sujet['sujet'], page['ville'], page['type'])
    
    return {"status": "success", "message": "Sujet modifier avec succès"}

class VilleUpdate(BaseModel):
    ville: str

@celery_app.task
def update_ville_celery(id: str, ville: str):
    asyncio.set_event_loop(global_loop)
    
    # Exécuter le code asynchrone dans cette boucle
    result = global_loop.run_until_complete(_async_update_ville(id,ville))
    
    return result
async def _async_update_ville(id: str, ville_new):
    if ville := db.ville.find_one({"_id": ObjectId(id)}):
        ville = await db.ville.find_one({"_id": ObjectId(id)})
        
        # Si la ville est trouvée
        if ville:
            # Affiche la ville actuelle
            print("LA VILLE AVANT LA MODIFICATION:")
            print(ville['ville'])
            pages_cursor = db.page.find({"ville": ville['ville']})

            for page in await pages_cursor.to_list(length=9999):
                print(page['_id'])
                mise_a_jour_contenu(str(page['id_page']),page['sujet'], ville_new, page['type'])
                db.page.update_one({"_id": ObjectId(page['_id'])}, {"$set": {"ville": ville_new}})

        db.ville.update_one({"_id": ObjectId(id)}, {"$set": {"ville": ville_new}})
        return {"status": "success", "message": "Ville modifier avec succès"}
    raise HTTPException(status_code=404, detail="Ville not found")

async def get_all_cities():
    ville_collection = db['ville']
    cities = []
    cursor = ville_collection.find({}, {"ville": 1, "_id": 0})
    async for doc in cursor:
        cities.append(doc['ville'])
    return cities


async def generate_content_for_all_cities(sujet, type ,categorie):
    print("ICI GENERATION CONTENU")
    all_cities = await get_all_cities()
    print("SUITE")
    for ville in all_cities:
        
        created_id = creation_page_contenu(sujet, ville, type)
        print("CREATE")
        page_data = {
            "id_page": created_id,
            "sujet": sujet,
            "ville": ville,
            "type": type,
            "categorie": categorie
        }
        result = db.page.insert_one(page_data)
        if not result:
            raise HTTPException(status_code=500, detail="Erreur lors de l'enregistrement des données de la page")

    return {"message": "Contenu généré et enregistré avec succès dans la collection page"}

async def get_all_subject():
    sujet_collection = db['sujet']
    sujets = []
    cursor = sujet_collection.find({}, {"sujet": 1, "type": 1, "categorie": 1, "_id": 0})
    async for doc in cursor:
        sujets.append([doc['sujet'],doc['type'],doc['categorie']])
    return sujets

async def generate_content_for_all_subject(ville):
    print("ICI GENERATION CONTENU")
    all_subject = await get_all_subject()
    print("SUITE")
    for sujet in all_subject:
        
        created_id = creation_page_contenu(sujet[0], ville, sujet[1])
        print("CREATE")
        page_data = {
            "id_page": created_id,
            "sujet": sujet,
            "ville": ville,
            "type": sujet[1],
            "categorie": sujet[2]
        }
        result = db.page.insert_one(page_data)
        if not result:
            raise HTTPException(status_code=500, detail="Erreur lors de l'enregistrement des données de la page")

    return {"message": "Contenu généré et enregistré avec succès dans la collection page"}

#API DU TEMPLATE SUJET

class Sujet(BaseModel):
    sujet: str

@celery_app.task
def ajouter_sujet_service(sujet: str):
    asyncio.set_event_loop(global_loop)
    
    # Exécuter le code asynchrone dans cette boucle
    result = global_loop.run_until_complete(_async_ajouter_sujet(sujet))
    
    return result
async def _async_ajouter_sujet(sujet: str):
    print("AJOUT SUJET")
    id_page = creation_page_contenu_service(sujet)
    sujet_data = {"sujet": sujet,
                  "id_page" : id_page}
    result = await db.sujet_service.insert_one(sujet_data)
    return {"id": str(result.inserted_id)}

@celery_app.task
def delete_sujet_celery(sujet_id: str):
    #asyncio.set_event_loop(global_loop)
    print("essui glace")
    # Exécuter le code asynchrone dans cette boucle
    result = global_loop.run_until_complete(_async_delete_sujet(sujet_id))
    
    return result

async def _async_delete_sujet(sujet_id: str):
    # Convertir sujet_id en ObjectId
    print("ZZZZ")
    print(sujet_id)

    try:
        obj_id = ObjectId(sujet_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid sujet_id format")
    
    # Trouver le sujet correspondant
    sujet = await db.sujet_service.find_one({"_id": obj_id})
    if sujet is None:
        raise HTTPException(status_code=404, detail="Sujet not found")

    delete_page(str(sujet['id_page']))
    # Supprimer le sujet
    result = await db.sujet_service.delete_one({"_id": obj_id})

    # Si aucun sujet n'a été supprimé (peut-être que l'id n'était pas correct), renvoyez une erreur
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Sujet not found")

    return {"status": "success", "message": "Sujet deleted successfully"}

@celery_app.task
def update_sujet_service_by_id_celery(sujet_id: str):
    asyncio.set_event_loop(global_loop)
    print("BL")
    # Exécuter le code asynchrone dans cette boucle
    result = global_loop.run_until_complete(_async_update_sujet_service_by_id(sujet_id))
    
    return result
async def _async_update_sujet_service_by_id(sujet_id: str):

    try:
        obj_id = ObjectId(sujet_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid sujet_id format")
    
    sujet = await db.sujet_service.find_one({"_id": obj_id})

    mise_a_jour_contenu_service(sujet['id_page'],sujet['sujet'])
    if sujet is None:
        raise HTTPException(status_code=404, detail="Sujet not found")

    # Convertir l'ObjectId en chaîne
    sujet["_id"] = str(sujet["_id"])

    return {"status": "success", "message": "Service mise à jour"}

class SujetUpdate(BaseModel):
    sujet: str

@celery_app.task
def update_sujet_service_celery(sujet_id: str, sujet: str):
    asyncio.set_event_loop(global_loop)

    # Exécuter le code asynchrone dans cette boucle
    result = global_loop.run_until_complete(_async_update_sujet(sujet_id, sujet))
    return result

        
async def _async_update_sujet(sujet_id: str, sujet: str):
    # Convertir sujet_id en ObjectId
    try:
        obj_id = ObjectId(sujet_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid sujet_id format")
    
    page = await db.sujet_service.find_one({"_id": obj_id})
    print("LA PAGE ")
    print(page)
    mise_a_jour_contenu_service(str(page['id_page']),sujet)

    # Mettre à jour le sujet
    result = await db.sujet_service.update_one({"_id": obj_id}, {"$set": {"sujet": sujet}})

    # Vérifier si la mise à jour a été effectuée avec succès
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Sujet not found")

    if result.modified_count == 0:
        return {"status": "no change", "message": "Sujet data was the same. No change made."}

    return {"status": "success", "message": "Sujet updated successfully"}

@celery_app.task
def delete_item_celery(collection_type: str, item_id: str):
    asyncio.set_event_loop(global_loop)
    
    # Exécuter le code asynchrone dans cette boucle
    result = global_loop.run_until_complete(_async_delete_item_celery(collection_type, item_id))
    
    return result

async def _async_delete_item_celery(collection_type: str, item_id: str):
    if collection_type not in ["ville", "sujet"]:
        raise HTTPException(status_code=400, detail="Invalid collection type")
    
    # Convertir item_id en ObjectId
    try:
        obj_id = ObjectId(item_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid item_id format")
    
    item = await db[collection_type].find_one({"_id": obj_id})
    # Utilisez la connexion à la base de données pour supprimer l'élément
    if collection_type == "sujet":
        print("SUJET")
        print(item["sujet"])
        # Supprimer toutes les pages qui ont le sujet correspondant
        page_sujet = db['page'].find({"sujet": item["sujet"]})
        print(page_sujet)
        async for page in page_sujet:
        # Convertir ObjectId en str pour la réponse JSON
            delete_page(str(page["id_page"]))
        await db['page'].delete_many({"sujet": item["sujet"]})
    elif collection_type == "ville":
        print(item["ville"])
        # Supprimer toutes les pages qui ont la ville correspondante
        page_ville = db['page'].find({"ville": item["ville"]})
        async for page in page_ville:
        # Convertir ObjectId en str pour la réponse JSON
            delete_page(str(page["id_page"]))
        await db['page'].delete_many({"ville": item["ville"]})
    result = await db[collection_type].delete_one({"_id": obj_id})

    # Si aucun élément n'a été supprimé (peut-être que l'id n'était pas correct), renvoyez une erreur
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Si tout se passe bien, renvoyez une réponse de succès
    return {"status": "success", "message": f"Item from {collection_type} deleted successfully"}