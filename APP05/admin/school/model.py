import uuid
from datetime import date
from typing import Optional, Dict
from pydantic import BaseModel, Field, Json

class m_school(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    school_name: str = Field(...)
    school_conPerson:str= Field(...)
    school_status:str=Field(...)
    
    
    
class schoolUpdate(BaseModel):
    school_name: Optional[str]
    school_conPerson: Optional[str]
    school_status: Optional[str]