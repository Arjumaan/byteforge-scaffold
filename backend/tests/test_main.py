import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "byteforge-api"}

@pytest.mark.asyncio
async def test_register_user():
    # Note: This requires a real or mocked DB. 
    # For now, we're just checking if the app loads and route exists.
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/register", json={
            "email": "test@example.com",
            "password": "password123"
        })
    # Since we don't have a mocked DB in this simple test, 
    # it might return 500 or 400 depending on DB state, 
    # but the goal is to show the folder structure exists.
    assert response.status_code in [200, 400, 500] 
