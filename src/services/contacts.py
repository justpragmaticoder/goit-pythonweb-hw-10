from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.contacts import ContactRepository
from src.schemas import ContactModel


class ContactService:
    def __init__(self, db: AsyncSession):
        self._repository = ContactRepository(db)

    async def create_contact(self, data: ContactModel):
        existing_contact = await self._repository.does_contact_exist(data.email, data.phone_number)
        if existing_contact:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Contact with email '{data.email}' or phone '{data.phone_number}' already exists."
            )
        return await self._repository.create_contact(data)

    async def list_contacts(self, first_name: str = "", last_name: str = "", email: str = "", skip: int = 0, limit: int = 100):
        filters = {"first_name": first_name, "last_name": last_name, "email": email}
        return await self._repository.get_contacts(**filters, skip=skip, limit=limit)

    async def retrieve_contact(self, contact_id: int):
        contact = await self._repository.get_contact_by_id(contact_id)
        if not contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Contact with ID {contact_id} not found."
            )
        return contact

    async def modify_contact(self, contact_id: int, data: ContactModel):
        updated_contact = await self._repository.update_contact(contact_id, data)
        if not updated_contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unable to update contact with ID {contact_id}. It may not exist."
            )
        return updated_contact

    async def delete_contact(self, contact_id: int):
        deleted_contact = await self._repository.remove_contact(contact_id)
        if not deleted_contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unable to delete contact with ID {contact_id}. It may not exist."
            )
        return deleted_contact

    async def list_upcoming_birthdays(self, days: int):
        return await self._repository.get_upcoming_birthdays(days)