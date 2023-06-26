from fastapi import APIRouter, Body, Request, Form, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import uuid
from app.app04.admin.std.model import m_std,stdUpdate

admin_std_api = APIRouter()

#create
@admin_std_api.post("/", response_description="Create a new std", status_code=status.HTTP_201_CREATED,response_model=m_std)
async def create_student(request: Request, p_std: m_std = Body(...)):
    j_std = jsonable_encoder(p_std)
    new_std = request.app.database["students"].insert_one(j_std)
    created_std = request.app.database["students"].find_one(
        {"_id": new_std.inserted_id}
    )

    return created_std
    
#list
@admin_std_api.get("/", response_description="List all std")
def list_std(request: Request):
    students = list(request.app.database["students"].find({}))
    print(students)
    return {"students":students}
    
#delete
@admin_std_api.delete("/{id}", response_description="Delete a std")
def delete_std(id: str, request: Request, response: Response):
    delete_result = request.app.database["students"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"std with ID {id} not found")
    
#find
@admin_std_api.get("/{id}", response_description="Get a single std by id")
def find_std(id: str, request: Request):
    if (std := request.app.database["students"].find_one({"_id": id})) is not None:
        return std
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"std with ID {id} not found")
    
#UPDATE 
@admin_std_api.post("/{id}", response_description="Update a std" )
async def update_std(id: str, request: Request, std: stdUpdate = Body(...)):
    std = {k: v for k, v in std.dict().items() if v is not None}
    update_result = request.app.database["students"].update_one(
        {"_id": id}, {"$set": std}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"std with ID {id} not found")

    if (
        existing_std := request.app.database["students"].find_one({"_id": id})
    ) is not None:
        return existing_std

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"std with ID {id} not found")
    
