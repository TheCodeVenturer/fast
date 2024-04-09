from pydantic import BaseModel, Field
from typing import Optional

class Address(BaseModel):
    city: str = Field(..., description="City of the student's address")
    country: str = Field(..., description="Country of the student's address")

class StudentBase(BaseModel):
    name: str = Field(..., description="Name of the student")
    age: int = Field(..., description="Age of the student")
    address: Address = Field(..., description="Address of the student")

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    name: Optional[str] = Field(None, description="Updated name of the student")
    age: Optional[int] = Field(None, description="Updated age of the student")
    address: Optional[Address] = Field(None, description="Updated address of the student")

class StudentInDB(StudentBase):
    id: str = Field(..., description="Unique identifier of the student")

class StudentOut(StudentBase):
    pass
