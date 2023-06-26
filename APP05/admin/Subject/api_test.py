import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from dotenv import dotenv_values
from pymongo import MongoClient
from app.app04.main import app

config = dotenv_values(".env")
app.database = app.mongodb_client[app.dbname + "_test"]

#TEST CASE FOR CREATE#
def test_create_Subject(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('Testing Subject create...')
            response = client.post("/api/admin/Subject/",json={"title":"English","desc":"chapter1"})
            assert response.status_code == 201
            body = response.json()
            assert body.get("title") == "English"
            assert body.get("desc") == "chapter1"
            assert "_id" in body
  
  
#TEST CASE FOR LIST       
def test_get_Subject():
    with TestClient(app) as client:
        get_Subjects_response = client.get("/api/admin/Subject/")
        assert get_Subjects_response.status_code == 200
             
  
#TEST CASE FOR Find
def test_get_Subject():
    with TestClient(app) as client:
        new_Subject = client.post("/api/admin/Subject/",json={"title":"English","desc":"chapter1"}).json()

        get_Subject_response = client.get("/api/admin/Subject/" + new_Subject.get("_id"))
        assert get_Subject_response.status_code == 200
        assert get_Subject_response.json() == new_Subject

  
#TEST CASE FOR DELETE 
def test_delete__Subject():
    with TestClient(app) as client:
        new_Subject = client.post("/api/admin/Subject/",json={"title":"English","desc":"chapter1"}).json()

        delete_Subject_response = client.delete("/api/admin/Subject/" + new_Subject.get("_id"))
        assert delete_Subject_response.status_code == 204

#TEST CASE FOR UPDATE
def test_update_title(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            new_title= client.post("/api/admin/Subject",json={"title":"English","desc":"chapter1"}).json()
 
            response = client.post("/api/admin/Subject/" + new_title.get("_id"), json={"title": "English - Updated"})
            assert response.status_code == 200
            assert response.json().get("title") == "English - Updated"


