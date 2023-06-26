import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from dotenv import dotenv_values
from pymongo import MongoClient
from app.app04.main import app

config = dotenv_values(".env")
app.database = app.mongodb_client[app.dbname + "_test"]

from app.app04.admin.cls.api import admin_cls_api as admin_cls_apiroutes
app.include_router(admin_cls_apiroutes, tags=["clses"], prefix="/api/admin/cls")

#TEST CASE FOR CREATE#
def test_create_cls(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('Testing cls create...')
            response = client.post("/api/admin/cls/",json={"title":"tech", "desc":"New Cls"})
            assert response.status_code == 201
            
            body = response.json()
            
            assert body.get("title") == "tech"
            assert body.get("desc") == "New Cls"           
            assert "_id" in body
            
#TEST CASE FOR LIST#        
def test_get_cls():
    with TestClient(app) as client:
        get_clses_response = client.get("/api/admin/cls/")
        assert get_clses_response.status_code == 200
        
#TEST CASE FOR DELETE#       
def test_delete_cls(capsys):
    with TestClient(app) as client:
       with capsys.disabled():

        new_cls = client.post("/api/admin/cls/", json={"title":"tech", "desc":"New Cls"}).json()
        delete_cls_response = client.delete("/api/admin/cls/" + new_cls.get("_id"))
        assert delete_cls_response.status_code == 204
        
#TEST CASE FIND#       
def test_get_cls(capsys):
    with TestClient(app) as client:
       with capsys.disabled():

        new_cls = client.post("/api/admin/cls/", json={"title":"tech", "desc":"New Cls"}).json()

        get_cls_response = client.get("/api/admin/cls/" + new_cls.get("_id"))
        assert get_cls_response.status_code == 200
        assert get_cls_response.json() == new_cls
        
#TEST CASE FOR UPDATE#       
def test_update_desc(capsys):
    with TestClient(app) as client:
        with capsys.disabled():

            new_desc = client.post("/api/admin/cls/", json={"title":"tech", "desc":"New Cls"}).json()
            response = client.post("/api/admin/cls/" + new_desc.get("_id"), json={"desc": "New Cls- Updated"})
            assert response.status_code == 200
            assert response.json().get("desc") == "New Cls- Updated"

        
def test_update_title(capsys):
    with TestClient(app) as client:
        with capsys.disabled():

            new_title = client.post("/api/admin/cls/", json={"title":"tech", "desc":"New Cls"}).json()
            response = client.post("/api/admin/cls/" + new_title.get("_id"), json={"title": "tech- Updated"})
            assert response.status_code == 200
            assert response.json().get("title") == "tech- Updated"

        
