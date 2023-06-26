import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from dotenv import dotenv_values
from pymongo import MongoClient
from app.app04.main import app

config = dotenv_values(".env")
app.database = app.mongodb_client[app.dbname + "_test"]

from app.app04.admin.school.api import admin_school_api as admin_school_apiroutes
app.include_router(admin_school_apiroutes, tags=["schools"], prefix="/api/admin/school")


#TEST CASE FOR CREATE#
def test_create_school(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('Testing school create...')
            response = client.post("/api/admin/school/",json={"school_name": "DAV","school_conPerson": "Nikita","school_status":"Onboarded"})
            assert response.status_code == 201
            body = response.json()
            assert body.get("school_name") == "DAV"
            assert body.get("school_conPerson") == "Nikita"
            assert body.get("school_status") == "Onboarded"
            assert "_id" in body
            
            
#TEST CASE FOR LIST#        
def test_get_school():
    with TestClient(app) as client:
        get_schools_response = client.get("/api/admin/school/")
        assert get_schools_response.status_code == 200
        
        
#TEST CASE FOR DELETE#       
def test_delete_school(capsys):
    with TestClient(app) as client:
       with capsys.disabled():

        new_school = client.post("/api/admin/school/", json={"school_name": "DAV","school_conPerson": "Nikita","school_status":"Onboarded"}).json()
        delete_school_response = client.delete("/api/admin/school/" + new_school.get("_id"))
        assert delete_school_response.status_code == 204
        

#TEST CASE FIND#       
def test_get_school(capsys):
    with TestClient(app) as client:
       with capsys.disabled():

        new_school = client.post("/api/admin/school/", json={"school_name": "DAV","school_conPerson": "Nikita","school_status":"Onboarded"}).json()

        get_school_response = client.get("/api/admin/school/" + new_school.get("_id"))
        assert get_school_response.status_code == 200
        assert get_school_response.json() == new_school
        
def test_get_school_unexisting(capsys):
   with TestClient(app) as client:
        with capsys.disabled():
            get_school_response = client.get("/api/admin/school/unexisting_id")
            assert get_school_response.status_code == 404
            

#TEST CASE FOR UPDATE#       
def test_update_school_name(capsys):
    with TestClient(app) as client:
        with capsys.disabled():

            new_school = client.post("/api/admin/school/", json={"school_name": "DAV","school_conPerson": "Nikita","school_status":"Onboarded"}).json()
            response = client.post("/api/admin/school/" + new_school.get("_id"), json={"school_name": "DAV-Updated"})
            assert response.status_code == 200
            assert response.json().get("school_name") == "DAV-Updated"            
            
def test_update_school_conPerson(capsys):
    with TestClient(app) as client:
        with capsys.disabled():

            new_school = client.post("/api/admin/school/", json={"school_name": "DAV","school_conPerson": "Nikita","school_status":"Onboarded"}).json()
            response = client.post("/api/admin/school/" + new_school.get("_id"), json={"school_conPerson": "Nikita-Updated"})
            assert response.status_code == 200
            assert response.json().get("school_conPerson") == "Nikita-Updated"            
            
def test_update_school_status(capsys):
    with TestClient(app) as client:
        with capsys.disabled():

            new_school = client.post("/api/admin/school/", json={"school_name": "DAV","school_conPerson": "Nikita","school_status":"Onboarded"}).json()
            response = client.post("/api/admin/school/" + new_school.get("_id"), json={"school_status": "Onboarded-Updated"})
            assert response.status_code == 200
            assert response.json().get("school_status") == "Onboarded-Updated"            