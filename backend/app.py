from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import uvicorn

app = FastAPI(title="TeamTrack API", version="0.1.0")

# CORS for frontend at localhost:5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
employees = []
next_id = 1

# Seed data matching frontend fields
SEED = [
    {"name":"John Doe","email":"john.doe@company.com","department":"Engineering","position":"Software Engineer","status":"Active"},
    {"name":"Jane Smith","email":"jane.smith@company.com","department":"Marketing","position":"Marketing Manager","status":"Active"},
    {"name":"Robert Johnson","email":"robert.johnson@company.com","department":"Engineering","position":"DevOps Engineer","status":"On Leave"},
]

class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: str
    position: Optional[str] = None
    status: Optional[str] = "Active"

class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: str
    department: str
    position: Optional[str] = None
    status: Optional[str] = "Active"

@app.on_event("startup")
async def seed():
    global next_id
    for item in SEED:
        employees.append({"id": next_id, **item})
        next_id += 1

@app.get("/employees", response_model=List[EmployeeResponse])
def list_employees():
    return employees

@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int):
    for e in employees:
        if e["id"] == employee_id:
            return e
    raise HTTPException(status_code=404, detail="Employee not found")

@app.post("/employees", response_model=EmployeeResponse, status_code=201)
def create_employee(item: EmployeeCreate):
    global next_id
    new_employee = {
        "id": next_id,
        "name": item.name,
        "email": item.email,
        "department": item.department,
        "position": item.position,
        "status": item.status,
    }
    employees.append(new_employee)
    next_id += 1
    return new_employee

@app.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, item: EmployeeCreate):
    for e in employees:
        if e["id"] == employee_id:
            e["name"] = item.name
            e["email"] = item.email
            e["department"] = item.department
            e["position"] = item.position
            e["status"] = item.status
            return e
    raise HTTPException(status_code=404, detail="Employee not found")

@app.delete("/employees/{employee_id}", status_code=204)
def delete_employee(employee_id: int):
    for idx, e in enumerate(employees):
        if e["id"] == employee_id:
            employees.pop(idx)
            return
    raise HTTPException(status_code=404, detail="Employee not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
