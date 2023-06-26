from fastapi import APIRouter, Body, Request, Form, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import uuid
from app.app04.admin.Subject.model import m_Subject

student_subjects_api = APIRouter()


@student_subjects_api.get("/", response_description="find a std")
def list_subjects(request: Request, response: Response):
    # top_Subjects = list(request.app.database["Topics"].find({},{"_id":0,"s_subject":1,"s_subjecttitle":1}))
    unq_Subjects = list(request.app.database["Topics"].distinct("s_subjecttitle"))
    print(unq_Subjects)
    return {"Subjects":unq_Subjects}
   