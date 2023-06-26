from fastapi import  APIRouter, Body, Request, Form, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import uuid
from app.app04.admin.Topic.model import m_Topic, m_TopicUpdate

admin_Topic_api = APIRouter()

#CREATE FOR Topic
@admin_Topic_api.post("/", response_description="Create a new Topic", status_code=status.HTTP_201_CREATED, response_model=m_Topic)
async def create_Topic(request: Request, p_Topic: m_Topic = Body(...)):
    Topic = await request.json()
    Topic["_id"] = str(uuid.uuid4())
    Topic = jsonable_encoder(Topic)
    print(Topic)
    new_Topic = request.app.database["Topics"].insert_one(Topic)
    created_Topic = request.app.database["Topics"].find_one(
        {"_id": new_Topic.inserted_id}
    )

    return created_Topic


#List FOR Topic
@admin_Topic_api.get("/", response_description="List all Topic")
def list_Topic(request: Request):
    Topic = list(request.app.database["Topics"].find({}))
    print(Topic)
    return {"Topic":Topic}
 
#Find FOR Topic
@admin_Topic_api.get("/{id}", response_description="Get a single Topic by id", response_model=m_Topic)
def find_Topic(id: str, request: Request):
    if (Topic := request.app.database["Topics"].find_one({"_id": id})) is not None:
        return Topic

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Topic with ID {id} not found")
    
    
#DELETE FOR TOPIC  
@admin_Topic_api.delete("/{id}", response_description="Delete a ")
def delete_Topic(id: str, request: Request, response: Response):
    delete_result = request.app.database["Topics"].delete_one({"_id": id})
    Topic= request.app.database["Topics"].delete_many({"p_id":id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Topic with ID {id} not found")  

    
#UPDATE FOR TOPIC
@admin_Topic_api.post("/{id}", response_description="Update a Topic", response_model=m_Topic)
async def update_Topic(id: str, request: Request, Topic: m_TopicUpdate = Body(...)):
    p = await request.json()
    print(p)
    
    #Topic = {k: v for k, v in Topic.dict().items() if v is not None}

    #if len(Topic) >= 1:
    update_result = request.app.database["Topics"].update_one(
        {"_id": id}, {"$set": p}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Topic with ID {id} not found")

    if (
        existing_Topic := request.app.database["Topics"].find_one({"_id": id})
    ) is not None:
        return existing_Topic

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Topic with ID {id} not found")
