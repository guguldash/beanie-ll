import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from dotenv import dotenv_values
from pymongo import MongoClient
from app.app04.main import app

config = dotenv_values(".env")
app.database = app.mongodb_client[app.dbname + "_test"]

#TEST CASE FOR CREATE#
def test_create_Topic(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('Testing Topic create...')
            response = client.post("/api/admin/Topic/",json={"title":"Math","SL_NO":3,"Topic_id":234,"s_subject":"english","s_class":"social","s_subjecttitle":"math","s_classtitle":"urdu"})
            assert response.status_code == 201
            body = response.json()
            assert body.get("title") == "Math"
            assert body.get("SL_NO") == 3
            assert body.get("Topic_id") == 234
            assert body.get("s_subject") == "english"
            assert body.get("s_class") == "social"
            assert body.get("s_subjecttitle") == "math"
            assert body.get("s_classtitle") == "urdu"
            assert "_id" in body
            
            
#TEST CASE FOR LIST        
def test_get_Topic():
    with TestClient(app) as client:
        get_Topics_response = client.get("/api/admin/Topic/")
        assert get_Topics_response.status_code == 200
             
  
#TEST CASE FOR Find
def test_get_Topic():
    with TestClient(app) as client:
        new_Topic = client.post("/api/admin/Topic/",json={"title":"Math","SL_NO":3,"Topic_id":234,"s_subject":"english","s_class":"social","s_subjecttitle":"math","s_classtitle":"urdu"}).json()
        get_Topic_response = client.get("/api/admin/Topic/" + new_Topic.get("_id"))
        assert get_Topic_response.status_code == 200
        assert get_Topic_response.json() == new_Topic


#TEST CASE FOR DELETE 
def test_delete_Topic():
    with TestClient(app) as client:
        new_Topic = client.post("/api/admin/Topic/",json={"title":"Math","SL_NO":3,"Topic_id":234,"s_subject":"english","s_class":"social","s_subjecttitle":"math","s_classtitle":"urdu"}).json()
        delete_Topic_response = client.delete("/api/admin/Topic/"        
        + new_Topic.get("_id"))
        assert delete_Topic_response.status_code == 204
        

#TEST CASE FOR UPDATE
def test_update_title(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            new_title= client.post("/api/admin/Topic",json={"title":"Math","SL_NO":3,"Topic_id":234,"s_subject":"english","s_class":"social","s_subjecttitle":"math","s_subjecttitle":"math","s_classtitle":"urdu"}).json()
            response = client.post("/api/admin/Topic/" + new_title.get("_id"), json={"title": "Math - Updated"})
            assert response.status_code == 200
            assert response.json().get("title") == "Math - Updated"


#TEST CASE FOR UPDATE
def test_update_s_subject(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            new_s_subject= client.post("/api/admin/Topic",json={"title":"Math","SL_NO":3,"Topic_id":234,"s_subject":"english","s_class":"social","s_subjecttitle":"math","s_classtitle":"urdu"}).json()
            response = client.post("/api/admin/Topic/" + new_s_subject.get("_id"), json={"s_subject": "Math - Updated"})
            assert response.status_code == 200
            assert response.json().get("s_subject") == "Math - Updated"


#TEST CASE FOR UPDATE
def test_update_s_class(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            new_s_class= client.post("/api/admin/Topic",json={"title":"Math","SL_NO":3,"Topic_id":234,"s_subject":"english","s_class":"social","s_subjecttitle":"math","s_classtitle":"urdu"}).json()
            response = client.post("/api/admin/Topic/" + new_s_class.get("_id"), json={"s_class": "social - Updated"})
            assert response.status_code == 200
            assert response.json().get("s_class") == "social - Updated"
            
            
#TEST CASE FOR UPDATE
def test_update_s_subjecttitle(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            new_s_class= client.post("/api/admin/Topic",json={"title":"Math","SL_NO":3,"Topic_id":234,"s_subject":"english","s_class":"social","s_subjecttitle":"math","s_classtitle":"urdu"}).json()
            response = client.post("/api/admin/Topic/" + new_s_class.get("_id"), json={"s_subjecttitle": "math - Updated"})
            assert response.status_code == 200
            assert response.json().get("s_subjecttitle") == "math - Updated"


def test_update_s_classtitle(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            new_s_class= client.post("/api/admin/Topic",json={"title":"Math","SL_NO":3,"Topic_id":234,"s_subject":"english","s_class":"social","s_subjecttitle":"math","s_classtitle":"urdu"}).json()
            response = client.post("/api/admin/Topic/" + new_s_class.get("_id"), json={"s_classtitle": "urdu - Updated"})
            assert response.status_code == 200
            assert response.json().get("s_classtitle") == "urdu - Updated"
