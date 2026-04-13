from fastapi.testclient import TestClient
from app import main
from config.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database_engine import Base, get_db
import pytest


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
def create_test_file(client):
    response = client.post("/file/upload_file",
                            files={"file": ("test.txt", "content_test", "text/plain")})
    assert response.status_code == 201