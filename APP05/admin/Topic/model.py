import uuid
from datetime import date
from typing import Optional, Dict
from pydantic import BaseModel, Field, Json

class m_Topic(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(...)
    SL_NO: int = Field(...)
    Topic_id : int = Field(...)
    s_subject: str = Field(...)
    s_class: str = Field(...)
    s_subjecttitle : str = Field(...)
    s_classtitle: str = Field(...)
    
class m_TopicUpdate(BaseModel):
     title: Optional[str]
     SL_NO: Optional[int]
     Topic_id: Optional[int]
     s_subject: Optional[str]
     s_subjecttitle:Optional[str]
     s_class: Optional[str]
     s_classtitle: Optional[str]
    

    