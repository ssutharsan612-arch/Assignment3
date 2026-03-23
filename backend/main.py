from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from bson import ObjectId
from datetime import datetime
from jose import JWTError

from database import users, incidents
from models import UserCreate, Incident
from auth import hash_password, check_password
from jwt_utils import make_token, read_token

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

oauth2 = OAuth2PasswordBearer(tokenUrl="token")

# helper: turn MongoDB doc into JSON-safe dict
def fix(doc):
    doc["_id"] = str(doc["_id"])
    return doc

# helper: check token and return username
async def get_current_user(token: str = Depends(oauth2)):
    try:
        data = read_token(token)
        return data["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Not logged in")


# --- HEALTH ---
@app.get("/health")
async def health():
    return {"status": "ok"}


# --- REGISTER ---
@app.post("/register")
async def register(body: UserCreate):
    existing = await users.find_one({"username": body.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username taken")
    await users.insert_one({
        "username": body.username,
        "password_hash": hash_password(body.password),
        "role": "engineer"
    })
    return {"message": "User created"}


# --- LOGIN ---
@app.post("/token")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = await users.find_one({"username": form.username})
    if not user or not check_password(form.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Wrong username or password")
    token = make_token(user["username"])
    return {"access_token": token, "token_type": "bearer"}


# --- GET ALL INCIDENTS ---
@app.get("/incidents")
async def get_incidents():
    result = []
    async for doc in incidents.find():
        result.append(fix(doc))
    return result


# --- GET ONE INCIDENT ---
@app.get("/incidents/{id}")
async def get_incident(id: str):
    doc = await incidents.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Not found")
    return fix(doc)


# --- CREATE INCIDENT (login required) ---
@app.post("/incidents", status_code=201)
async def create_incident(body: Incident, user=Depends(get_current_user)):
    new = body.dict()
    new["created_at"] = str(datetime.utcnow())
    new["updated_at"] = str(datetime.utcnow())
    result = await incidents.insert_one(new)
    new["_id"] = str(result.inserted_id)
    return new


# --- UPDATE INCIDENT (login required) ---
@app.put("/incidents/{id}")
async def update_incident(id: str, body: Incident, user=Depends(get_current_user)):
    updated = body.dict()
    updated["updated_at"] = str(datetime.utcnow())
    await incidents.update_one({"_id": ObjectId(id)}, {"$set": updated})
    doc = await incidents.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Not found")
    return fix(doc)


# --- DELETE INCIDENT (login required) ---
@app.delete("/incidents/{id}")
async def delete_incident(id: str, user=Depends(get_current_user)):
    result = await incidents.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Not found")
    return {"message": "Deleted"}