import pytest
import os
from unittest.mock import patch, AsyncMock
from schemas import schemas_file
from database import models


def test_upload_file_succes(client, session, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    os.makedirs(tmp_path / "disc", exist_ok=True)

    file_content = b"Test content for upload_file endpoint!"
    expected_hash = '28c44fd3120551ce87b2825d23faafa468882eb56918c57ce38897049694e950'

    response = client.post("/file/upload_file",
                            files={"file": ("test.txt", file_content, "text/plain")})
    
    assert response.status_code == 201

    data = schemas_file.FileResponse(**response.json())
    assert data.hashed_content == expected_hash
    assert data.file_name == "test.txt"
    assert data.file_type == "text/plain"
    assert data.file_size == len(file_content)
    assert data.file_path == "disc/test.txt_28c44fd3"
    assert (tmp_path / "disc" / "test.txt_28c44fd3").exists()

    db_file = session.query(models.File).filter_by(file_name='test.txt').first()
    assert db_file is not None
    assert db_file.hashed_content == expected_hash  

def test_upload_the_same_name_files_different_content(client, session, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    os.makedirs(tmp_path / "disc", exist_ok=True)

    file_content1 = b"file content first"
    file_content2 = b"file content second"

    file1 = {"file": ("test.txt", file_content1, "text/plain")}
    file2 = {"file": ("test.txt", file_content2, "text/plain")}

    response1 = client.post("/file/upload_file",
                             files=file1)
    assert response1.status_code == 201
    data1 = schemas_file.FileResponse(**response1.json())
    assert data1.file_name == "test.txt"

    response2 = client.post("/file/upload_file", files=file2)
    assert response2.status_code == 201
    data2 = schemas_file.FileResponse(**response2.json())
    assert data2.file_name == "test.txt"

    assert data1.file_name == data2.file_name
    assert data1.hashed_content != data2.hashed_content 

    db_files = session.query(models.File).filter_by(file_name="test.txt").all()
    assert len(db_files) == 2

    assert (tmp_path / "disc" / f"test.txt_{data1.hashed_content[:8]}").exists()
    assert (tmp_path / "disc" / f"test.txt_{data2.hashed_content[:8]}").exists()

    assert data1.file_path != data2.file_path