import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from dotenv import dotenv_values
from pymongo import MongoClient
from app.app04.main import app

config = dotenv_values(".env")
app.database = app.mongodb_client[app.dbname + "_test"]

from app.app04.admin.std.api import admin_std_api as admin_std_apiroutes
app.include_router(admin_std_apiroutes, tags=["students"], prefix="/api/admin/std")

#TEST CASE FOR CREATE#
def test_create_std(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('Testing std create...')
            response = client.post("/api/admin/std/",json={"s_name":"naveen", "s_age": 22, "s_gender":"m", "s_dob":"10-08-2003", "s_rollno": 11,"s_class":"", "s_classtitle":""})
            assert response.status_code == 201
            
            body = response.json()
            
            assert body.get("s_name") == "naveen"
            assert body.get("s_dob") == "10-08-2003"
            assert body.get("s_age") ==  22
            assert body.get("s_gender") == "m"
            assert body.get("s_rollno") == 11
            assert body.get("s_class") == ""
            assert "_id" in body
            
#TEST CASE FOR LIST#        
def test_get_std():
    with TestClient(app) as client:
        get_students_response = client.get("/api/admin/std/")
        assert get_students_response.status_code == 200
        
#TEST CASE FOR DELETE#       
def test_delete_std(capsys):
    with TestClient(app) as client:
       with capsys.disabled():

        new_std = client.post("/api/admin/std/", json={"s_name":"naveen", "s_age": 22, "s_gender":"m", "s_dob":"10-08-2003", "s_rollno": 11,"s_class":"", "s_classtitle":""}).json()
        delete_std_response = client.delete("/api/admin/std/" + new_std.get("_id"))
        assert delete_std_response.status_code == 204
        
#TEST CASE FIND#       
def test_get_std(capsys):
    with TestClient(app) as client:
       with capsys.disabled():

        new_std = client.post("/api/admin/std/", json={"s_name":"naveen", "s_age": 22, "s_gender":"m", "s_dob":"10-08-2003", "s_rollno": 11,"s_class":"", "s_classtitle":""}).json()

        get_std_response = client.get("/api/admin/std/" + new_std.get("_id"))
        assert get_std_response.status_code == 200
        assert get_std_response.json() == new_std
        
#TEST CASE FOR UPDATE#       
def test_update_s_name(capsys):
    with TestClient(app) as client:
        with capsys.disabled():

            new_s_name = client.post("/api/admin/std/", json={"s_name":"naveen", "s_age": 22, "s_gender":"m", "s_dob":"10-08-2003", "s_rollno": 11,"s_class":"", "s_classtitle":""}).json()
            response = client.post("/api/admin/std/" + new_s_name.get("_id"), json={"s_name": "New navi- Updated"})
            assert response.status_code == 200
            assert response.json().get("s_name") == "New navi- Updated"

        
