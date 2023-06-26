import uuid
from datetime import date
from typing import Optional, Dict
from pydantic import BaseModel, Field, Json
from beanie import Document



class STD(Document, BaseModel):
    class Settings:
        name = "student_records"
    
    s_name: str = Field(...)
    s_dob: str = Field(...)
    s_age: int = Field(...)
    s_gender: str = Field(...)
    s_rollno: int = Field(...)
    s_class: str = Field(...) 
    s_classtitle: str = Field(...)
    
    
   
   
   