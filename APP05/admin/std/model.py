import uuid
from datetime import date
from typing import Optional, Dict
from pydantic import BaseModel, Field, Json

class m_std(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    s_name: str = Field(...)
    s_dob: str = Field(...)
    s_age: int = Field(...)
    s_gender: str = Field(...)
    s_rollno: int = Field(...)
    s_class: str = Field(...) 
    s_classtitle: str = Field(...)
    
class stdUpdate(BaseModel):
    s_name: Optional[str]
    s_dob: Optional[str]
    s_age: Optional[int]
    s_gender: Optional[str]
    s_rollno: Optional[int]
    s_class: Optional[str]
    s_classtitle: Optional[str]
    