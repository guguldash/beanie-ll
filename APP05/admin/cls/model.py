import uuid
from datetime import date
from typing import Optional, Dict
from pydantic import BaseModel, Field, Json

class m_cls(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(...)
    desc: str = Field(...)
    
class clsUpdate(BaseModel):
    title: Optional[str]
    desc: Optional[str]
    
 
    