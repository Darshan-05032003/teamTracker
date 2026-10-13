from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import os
import uvicorn

# MongoDB setup (requires pymongo; available locally? Check environment first)
try:
    import pymongo
    from pymongo import MongoClient
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False

app = FastAPI(title="TeamTrack API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection via environment (fail clearly; no silent in-memory fallback)
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "teamtrack")

if MONGODB_AVAILABLE:
    try:
        mongo_client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=2000)
        mongo_client.admin.command("ping")
        db = mongo_client[MONGODB_DB]
        employees_col = db["employees"]
    except Exception as exc:
        raise RuntimeError(
            f"MongoDB connection failed at {MONGODB_URI}. "
            f"Check that MongoDB is running and MONGODB_URI is correct. Error: {exc}"
        ) from exc
else:
    raise RuntimeError(
        "PyMongo is not installed. Install it (`pip install pymongo`) or check that the "
        "project environment is activated. MongoDB persistence requires PyMongo."
    )

class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: str
    position: Optional[str] = None
    status: Optional[str] = "Active"

class EmployeeResponse(BaseModel):
    id: int  # preserved for API compatibility; mapped from MongoDB _id externally in production
    name: str
    email: str
    department: str
    position: Optional[str] = None
    status: Optional[str] = "Active"

# Seed data matching frontend fields
SEED = [
    {"name":"John Doe","email":"john.doe@company.com","department":"Engineering","position":"Software Engineer","status":"Active"},
    {"name":"Jane Smith","email":"jane.smith@company.com","department":"Marketing","position":"Marketing Manager","status":"Active"},
    {"name":"Robert Johnson","email":"robert.johnson@company.com","department":"Engineering","position":"DevOps Engineer","status":"On Leave"},
]

@app.on_event("startup")
async def seed():
    # Clear and seed for consistency (in-memory behavior preserved; real MongoDB would use upsert or migration logic)
    # Note: for MongoDB persistence this replaces in-memory `employees` array with `employees_col`
    # Because MongoDB is unavailable in this environment, seed logic is kept minimal.
    # Actual persistence: insert if empty.
    if MONGODB_AVAILABLE:
        existing = employees_col.count_documents({})
        if existing == 0:
            for item in SEED:
                employees_col.insert_one({"id": existing + 1 + SEED.index(item), **item})  # sequential preserved

@app.get("/employees", response_model=List[EmployeeResponse])
def list_employees():
    if not MONGODB_AVAILABLE:
        raise HTTPException(status_code=503, detail="MongoDB not available; check MONGODB_URI and PyMongo.")
    docs = list(employees_col.find({}))
    # Map MongoDB _id to int `id` for response compatibility
    result = []
    for d in docs:
        d["id"] = d.get("id", d.get("_id"))
        # Ensure id is int where practical
        try:
            d["id"] = int(d["id"])
        except Exception:
            pass
        result.append(d)
    return result

@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int):
    if not MONGODB_AVAILABLE:
        raise HTTPException(status_code=503, detail="MongoDB not available; check MONGODB_URI and PyMongo.")
    doc = employees_col.find_one({"id": employee_id})
    if doc is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    doc["id"] = doc.get("id", doc.get("_id"))
    try:
        doc["id"] = int(doc["id"])
    except Exception:
        pass
    return doc

@app.post("/employees", response_model=EmployeeResponse, status_code=201)
def create_employee(item: EmployeeCreate):
    if not MONGODB_AVAILABLE:
        raise HTTPException(status_code=503, detail="MongoDB not available; check MONGODB_URI and PyMongo.")
    # Preserve sequential ID behavior using a counter collection or find max
    max_doc = employees_col.find_one(sort=[("id", -1)])
    new_id = (max_doc.get("id", 0) if max_doc else 0) + 1
    new_employee = {"id": new_id, "name": item.name, "email": item.email,
                    "department": item.department, "position": item.position, "status": item.status}
    result = employees_col.insert_one(new_employee)
    new_employee["id"] = new_id
    return new_employee

@app.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, item: EmployeeCreate):
    if not MONGODB_AVAILABLE:
        raise HTTPException(status_code=503, detail="MongoDB not available; check MONGODB_URI and PyMongo.")
    result = employees_col.update_one(
        {"id": employee_id},
        {"$set": {"name": item.name, "email": item.email,
                  "department": item.department, "position": item.position,
                  "status": item.status}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    updated = employees_col.find_one({"id": employee_id})
    updated["id"] = updated.get("id", updated.get("_id"))
    try:
        updated["id"] = int(updated["id"])
    except Exception:
        pass
    return updated

@app.delete("/employees/{employee_id}", status_code=204)
def delete_employee(employee_id: int):
    if not MONGODB_AVAILABLE:
        raise HTTPException(status_code=503, detail="MongoDB not available; check MONGODB_URI and PyMongo.")
    result = employees_col.delete_one({"id": employee_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
