from fastapi import APIRouter, Body, Request, Form, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import uuid
from app.app04.admin.school.model import m_school,schoolUpdate

admin_school_api = APIRouter()

#create
@admin_school_api.post("/", response_description="Create a new school", status_code=status.HTTP_201_CREATED, response_model=m_school)
async def create_school(request: Request, p_school: m_school = Body(...)):
    school = jsonable_encoder(p_school)
    new_school = request.app.database["schools"].insert_one(school)
    created_school = request.app.database["schools"].find_one(
        {"_id": new_school.inserted_id}
    )

    return created_school
#List  
@admin_school_api.get("/", response_description="List all school")
def list_school(request: Request):
    school = list(request.app.database["schools"].find({}))
    print(school)
    return {"school":school}
    
    
#delete
@admin_school_api.delete("/{id}", response_description="Delete a school")
def delete_school(id: str, request: Request, response: Response):
    delete_result = request.app.database["schools"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"school with ID {id} not found")


#find
@admin_school_api.get("/{id}", response_description="Get a single school by id")
def find_school(id: str, request: Request):
    if (school := request.app.database["schools"].find_one({"_id": id})) is not None:
        return school
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"school with ID {id} not found")
    

#UPDATE 
@admin_school_api.post("/{id}", response_description="Update a school",)
async def update_school(id: str, request: Request, school: schoolUpdate = Body(...)):
    school = {k: v for k, v in school.dict().items() if v is not None}
    update_result = request.app.database["schools"].update_one(
        {"_id": id}, {"$set": school}
    )
    if update_result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"school with ID {id} not found")
    if (
        existing_school := request.app.database["schools"].find_one({"_id": id})
    ) is not None:
        return existing_school
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"school with ID {id} not found")
    