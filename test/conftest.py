from fastapi.testclient import TestClient
from app import main
from config.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database_engine import Base, get_db
import pytest
import os
from database import models



SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    main.app.dependency_overrides[get_db] = override_get_db
    yield TestClient(main.app)

@pytest.fixture()
def create_test_file(client, tmp_path, monkeypatch):
    """

    Create test file, add to database and on disc

    """
    monkeypatch.chdir(tmp_path)
    os.makedirs(tmp_path / "disc", exist_ok=True)

    res = client.post("/file/upload_file",
                            files={"file": ("test1.txt", b"content_test", "text/plain")})
    
    assert res.status_code == 201
    return res.json()

@pytest.fixture()
def check_file_in_db(session):
    """

    Check if file exists in database:
    file in database -> True
    file is not in database -> False

    """
    def _check(file_id):
        file = session.query(models.File).filter(models.File.id == file_id).first()

        if file is None:
            return False
        else:
            return True
    return _check 