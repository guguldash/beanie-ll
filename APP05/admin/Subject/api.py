from fastapi import  APIRouter, Body, Request, Form, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import uuid
from app.app04.admin.Subject.model import m_Subject, m_SubjectUpdate

admin_Subject_api = APIRouter()

#CREATE FOR SUBJECT
@admin_Subject_api.post("/", response_description="Create a new Subject", status_code=status.HTTP_201_CREATED, response_model=m_Subject)
async def create_Subject(request: Request, p_Subject: m_Subject = Body(...)):
    Subject = await request.json()
    Subject["_id"] = str(uuid.uuid4())
    Subject = jsonable_encoder(Subject)
    print(Subject)
    new_Subject = request.app.database["Subjects"].insert_one(Subject)
    created_Subject = request.app.database["Subjects"].find_one(
        {"_id": new_Subject.inserted_id}
    )

    return created_Subject

#List FOR SUBJECT
@admin_Subject_api.get("/", response_description="List all Subject")
def list_Subject(request: Request):
    Subject = list(request.app.database["Subjects"].find({}))
    print(Subject)
    return {"Subject":Subject}
 
 
#Find FOR SUBJECT
@admin_Subject_api.get("/{id}", response_description="Get a single Subject by id", response_model=m_Subject)
def find_Subject(id: str, request: Request):
    if (Subject := request.app.database["Subjects"].find_one({"_id": id})) is not None:
        return Subject

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Subject with ID {id} not found")
    


#DELETE FOR SUBJECT   
@admin_Subject_api.delete("/{id}", response_description="Delete a ")
def delete_Subject(id: str, request: Request, response: Response):
    delete_result = request.app.database["Subjects"].delete_one({"_id": id})
    Subject= request.app.database["Subjects"].delete_many({"p_id":id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Subject with ID {id} not found")  


#UPDATE FOR Subject
@admin_Subject_api.post("/{id}", response_description="Update a Subject", response_model=m_Subject)
async def update_Subject(id: str, request: Request, Subject: m_SubjectUpdate = Body(...)):
    p = await request.json()
    print(p)
    
    #Subject = {k: v for k, v in Subject.dict().items() if v is not None}

    #if len(Subject) >= 1:
    update_result = request.app.database["Subjects"].update_one(
        {"_id": id}, {"$set": p}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Subject with ID {id} not found")

    if (
        existing_Subject := request.app.database["Subjects"].find_one({"_id": id})
    ) is not None:
        return existing_Subject

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Subject with ID {id} not found")
