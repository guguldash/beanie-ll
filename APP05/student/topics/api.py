from fastapi import APIRouter, Body, Request, Form, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import uuid
from app.app04.admin.Topic.model import m_Topic

student_topics_api = APIRouter()



@student_topics_api.get("/", response_description="List all the topics")
def list_topics(request: Request, response: Response):
    Topics = list(request.app.database["Topics"].find({}))
    print(Topics)
    return {"Topics":Topics}