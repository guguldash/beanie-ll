from fastapi import APIRouter, Body, Request, Form, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import uuid
from app.app04.admin.cls.model import m_cls,clsUpdate

admin_cls_api = APIRouter()

#create
@admin_cls_api.post("/", response_description="Create a new cls", status_code=status.HTTP_201_CREATED,response_model=m_cls)
async def create_class(request: Request, p_cls: m_cls = Body(...)):
    j_cls = jsonable_encoder(p_cls)
    new_cls = request.app.database["clses"].insert_one(j_cls)
    created_cls = request.app.database["clses"].find_one(
        {"_id": new_cls.inserted_id}
    )

    return created_cls
    
#list
@admin_cls_api.get("/", response_description="List all cls")
def list_cls(request: Request):
    clses = list(request.app.database["clses"].find({}))
    print(clses)
    return {"clses":clses}
    
#delete
@admin_cls_api.delete("/{id}", response_description="Delete a cls")
def delete_cls(id: str, request: Request, response: Response):
    delete_result = request.app.database["clses"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"cls with ID {id} not found")
    
#find
@admin_cls_api.get("/{id}", response_description="Get a single cls by id")
def find_cls(id: str, request: Request):
    if (cls := request.app.database["clses"].find_one({"_id": id})) is not None:
        return cls
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"cls with ID {id} not found")
    
#UPDATE 
@admin_cls_api.post("/{id}", response_description="Update a cls" )
async def update_cls(id: str, request: Request, cls: clsUpdate = Body(...)):
    cls = {k: v for k, v in cls.dict().items() if v is not None}
    update_result = request.app.database["clses"].update_one(
        {"_id": id}, {"$set": cls}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"cls with ID {id} not found")

    if (
        existing_cls := request.app.database["clses"].find_one({"_id": id})
    ) is not None:
        return existing_cls

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"cls with ID {id} not found")

    

    