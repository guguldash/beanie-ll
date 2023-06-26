import os
from fastapi import FastAPI, Request, Form
from dotenv import load_dotenv
from fastapi.responses import FileResponse
from db import init
from student2.std import STD


load_dotenv()

app = FastAPI()

@app.on_event("startup")
async def app_init():
    await init()


@app.post("/std")
async def new_student_create_request(req: Request, data: STD) -> STD:
    print(f"......", data)
    
    # saving sattud into db
    await data.insert()
    
    return data

 
@app.get("/std")
async def get_all_student_records(req: Request) -> list[STD]:
    
    # saving sattud into db
    data = await STD.find_many().to_list()
    
    return data