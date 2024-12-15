from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_db
from src.schemas import ContactModel, ContactResponse
from src.services.contacts import ContactService

router = APIRouter(prefix="/contacts", tags=["contacts"])


# Dependency to provide a ContactService instance
def get_contact_service(db: AsyncSession = Depends(get_db)) -> ContactService:
    return ContactService(db)


# Utility function to handle not-found errors
def raise_not_found_error(detail: str = "Contact not found"):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail
    )


@router.get("/birthdays", response_model=List[ContactResponse])
async def get_upcoming_birthdays(
    days: int = Query(default=7, ge=1),
    contact_service: ContactService = Depends(get_contact_service),
):
    return await contact_service.list_upcoming_birthdays(days)


@router.get("/", response_model=List[ContactResponse])
async def get_all_contacts(
    first_name: str = "",
    last_name: str = "",
    email: str = "",
    skip: int = 0,
    limit: int = 100,
    contact_service: ContactService = Depends(get_contact_service),
):
    return await contact_service.list_contacts(first_name, last_name, email, skip, limit)


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: int,
    contact_service: ContactService = Depends(get_contact_service),
):
    contact = await contact_service.retrieve_contact(contact_id)
    if contact is None:
        raise_not_found_error()
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
    body: ContactModel,
    contact_service: ContactService = Depends(get_contact_service),
):
    return await contact_service.create_contact(body)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    body: ContactModel,
    contact_id: int,
    contact_service: ContactService = Depends(get_contact_service),
):
    contact = await contact_service.modify_contact(contact_id, body)
    if contact is None:
        raise_not_found_error()
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(
    contact_id: int,
    contact_service: ContactService = Depends(get_contact_service),
):
    contact = await contact_service.delete_contact(contact_id)
    if contact is None:
        raise_not_found_error()
    return contact