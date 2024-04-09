from fastapi import FastAPI, HTTPException, Path, Query, Body
from pymongo import MongoClient
from pydantic import BaseModel

from typing import List
from uuid import uuid4

app = FastAPI()

# Connect to MongoDB
uri = "mongodb+srv://Nidhi:Password@cluster0.lmquvvg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)

# Access the database and collection
db = client.library_management
collection = db["students"]  

# Models
class Address(BaseModel):
    city: str
    country: str

class Student(BaseModel):
    name: str
    age: int
    address: Address

class StudentResponse(Student):
    id: str

# Routes
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Library Management System!"}


@app.post("/students", response_model=StudentResponse, status_code=201)
async def create_student(student: Student):
    student_id = str(uuid4()) 
    student_data = student.dict()
    student_data["_id"] = student_id  
    collection.insert_one(student_data)  
    return {"id": student_id, **student.dict()}



@app.get("/students", response_model=List[StudentResponse])
async def list_students(country: str = Query(None), age: int = Query(None)):
    query = {}
    if country:
        query["address.country"] = country
    if age:
        query["age"] = {"$gte": age}

    students = collection.find(query)
    return [{**student, "id": student["_id"]} for student in students]


@app.get("/students/{student_id}", response_model=StudentResponse)
async def get_student(student_id: str = Path(..., title="The ID of the student to retrieve")):
    try:
        student = collection.find_one({"_id": student_id})
        if student:
            return {**student, "id": student["_id"]}
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.patch("/students/{student_id}", response_model=StudentResponse)
async def update_student(student_id: str = Path(..., title="The ID of the student to update"), student_update: Student = Body(...)):
    existing_student = collection.find_one({"_id": student_id})
    if existing_student:

        collection.update_one({"_id": student_id}, {"$set": student_update.dict()})
        return {**student_update.dict(), "id": student_id}
    else:
        raise HTTPException(status_code=404, detail="Student not found")



@app.delete("/students/{student_id}", response_model=dict)
async def delete_student(student_id: str = Path(..., title="The ID of the student to delete")):
    result = collection.delete_one({"_id": student_id})
    if result.deleted_count == 1:
        return {"message": "Student deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Student not found")