"""
Example usage of FastAPI-Users integration.

This script demonstrates how to use the authentication system
in your FastAPI application.
"""

# Import based on backend selection
import os
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

BACKEND = os.getenv("FASTAPI_USERS_BACKEND", "sqlalchemy")

if BACKEND == "sqlalchemy":
    from app.auth.manager import current_active_user, current_superuser
    from app.auth.models import User
else:
    from app.auth.manager_beanie import current_active_user, current_superuser
    from app.auth.models_beanie import User


# Example Pydantic models
class ItemCreate(BaseModel):
    title: str
    description: str = None


class ItemResponse(BaseModel):
    id: int
    title: str
    description: str = None
    owner_id: str


# Example router showing protected endpoints
example_router = APIRouter(prefix="/examples", tags=["examples"])


@example_router.get("/protected")
async def protected_endpoint(user: User = Depends(current_active_user)):
    """Example of a protected endpoint requiring authentication."""
    return {
        "message": f"Hello {user.email}!",
        "user_id": str(user.id),
        "username": getattr(user, "username", "N/A"),
    }


@example_router.get("/admin-only")
async def admin_only_endpoint(user: User = Depends(current_superuser)):
    """Example of an admin-only endpoint."""
    return {"message": f"Hello admin {user.email}!", "is_superuser": user.is_superuser}


@example_router.post("/items", response_model=ItemResponse)
async def create_item(item: ItemCreate, user: User = Depends(current_active_user)):
    """Example of creating an item associated with the current user."""
    # This is a mock implementation
    # In a real app, you would save to database
    return ItemResponse(
        id=1, title=item.title, description=item.description, owner_id=str(user.id)
    )


@example_router.get("/items", response_model=List[ItemResponse])
async def get_user_items(user: User = Depends(current_active_user)):
    """Example of getting items for the current user."""
    # This is a mock implementation
    # In a real app, you would query the database
    return [
        ItemResponse(
            id=1,
            title="User's Item 1",
            description="This belongs to the current user",
            owner_id=str(user.id),
        )
    ]


# Example of using current user in existing endpoints
from fastapi import FastAPI

app = FastAPI()

# Include the example router
app.include_router(example_router)


# Example middleware that uses current user
@app.middleware("http")
async def add_user_info(request, call_next):
    """Example middleware that could use user information."""
    response = await call_next(request)
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
